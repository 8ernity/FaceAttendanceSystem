import os
import cv2
import time
from app.utils.helpers import DATASET_DIR

class DatasetManager:
    def __init__(self):
        self.dataset_dir = DATASET_DIR

    def capture_images(self, username, num_images=1, interval=0.5):
        """Captures a single high-quality reference image for a new user"""
        user_dir = os.path.join(self.dataset_dir, username)
        os.makedirs(user_dir, exist_ok=True)

        # Standard OpenCV cascade for fallback fast extraction
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            yield False, "Failed to open camera hardware."
            return

        count = 0
        yield True, f"Starting capture for '{username}'. Please look directly at the camera..."
        time.sleep(1)

        while count < num_images:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to grayscale for faster detection 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(150, 150))

            if len(faces) > 0:
                # Take largest face
                faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
                (x, y, w, h) = faces[0]
                
                # Expand box slightly
                pad_x, pad_y = int(w * 0.15), int(h * 0.15)
                x1, y1 = max(0, x - pad_x), max(0, y - pad_y)
                x2, y2 = min(frame.shape[1], x + w + pad_x), min(frame.shape[0], y + h + pad_y)

                # Save face crop to dataset
                face_img = frame[y1:y2, x1:x2]
                img_path = os.path.join(user_dir, f"{username}_reference.jpg")
                cv2.imwrite(img_path, face_img)
                count += 1
                
                yield True, f"Reference image captured for {username}."
            
            time.sleep(0.1)

        cap.release()
        yield True, f"Finished capturing reference for {username}."
