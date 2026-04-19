import os
import cv2
import pickle
import face_recognition
import numpy as np
import time
from app.utils.helpers import ENCODINGS_DIR, play_alert
from app.core.attendance import AttendanceLogger
from app.core.cloudinary_manager import CloudinaryManager

class Recognizer:
    def __init__(self):
        self.cloud_manager = CloudinaryManager()
        self.logger = AttendanceLogger()
        self.data = None
        self.is_running = False

    def load_encodings(self):
        """Loads face encodings from Local Storage (CloudinaryManager)"""
        try:
            # Note: Initialization should have happened in main.py
            data = self.cloud_manager.fetch_all_users()
            if data and data["names"]:
                self.data = data
                return True
            return False
        except Exception as e:
            print(f"Data load error: {e}")
            return False

    def start_recognition(self):
        """Generates video frames and yields them with bounding boxes"""
        if not self.load_encodings() or not self.data or len(self.data["encodings"]) == 0:
            yield False, "Model not trained! Please add users and train first.", None
            return

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW avoids MSMF warnings on Windows
        if not cap.isOpened():
             yield False, "Could not open webcam. Check hardware connections.", None
             return

        self.is_running = True
        yield True, "Camera active. Looking for faces...", None

        pTime = 0 # For FPS
        marked_recently = {} # name -> timestamp

        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame = cv2.flip(frame, 1) # Mirror image

            # Downscale frame for faster face location processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Find all face locations and encodings in current frame
            faces = face_recognition.face_locations(rgb_small_frame)
            try:
                encodings = face_recognition.face_encodings(rgb_small_frame, faces)
            except (MemoryError, Exception):
                # Skip frame if encoding fails (e.g. memory spike)
                yield True, "Running", frame
                continue

            for face_loc, face_encoding in zip(faces, encodings):
                top, right, bottom, left = face_loc
                # Scale locations back up
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                name = "Unknown"
                confidence = 0
                color = (0, 0, 255) # Red for Unknown

                if self.data:
                    face_distances = face_recognition.face_distance(self.data["encodings"], face_encoding)
                    
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        best_distance = face_distances[best_match_index]
                        
                        # Threshold tuning: 0.5 is strict, 0.6 is default
                        if best_distance < 0.55:
                            name = self.data["names"][best_match_index]
                            confidence = round((1.0 - best_distance) * 100, 1)
                            color = (0, 255, 0) # Green for Known
                            
                            # Debounce: avoid duplicate marks within 15 seconds
                            current_time = time.time()
                            if name not in marked_recently or (current_time - marked_recently[name] > 15):
                                marked_recently[name] = current_time
                                success, msg = self.logger.mark_attendance(name)
                                if success:
                                    # We could yield messages to the UI, but simple print is fine, 
                                    # UI reads CSV or relies on sound alerts.
                                    pass 
                        else:
                            # Play unknown error beep on first detection
                            if "Unknown" not in marked_recently or (time.time() - marked_recently["Unknown"] > 5):
                                marked_recently["Unknown"] = time.time()
                                play_alert(success=False)

                # Draw UI overlays on the frame
                # 1. Bounding box
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # 2. Label background plate
                cv2.rectangle(frame, (left, bottom - (35 if name != "Unknown" else 30)), (right, bottom), color, cv2.FILLED)
                
                # 3. Label text
                font = cv2.FONT_HERSHEY_DUPLEX
                label = f"{name} {confidence}%" if name != "Unknown" else name
                cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.6, (0,0,0) if color==(0,255,0) else (255,255,255), 1)

            # Draw Performance Metics
            cTime = time.time()
            fps = 1 / (cTime - pTime) if pTime > 0 else 0
            pTime = cTime
            cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            yield True, "Running", frame

        cap.release()
        yield True, "Stopped", None
        
    def stop(self):
        self.is_running = False
