import os
import cv2
import pickle
import face_recognition
from app.utils.helpers import DATASET_DIR, ENCODINGS_DIR

class Encoder:
    def __init__(self):
        pass

    def generate_encoding(self, image_path):
        """Generates face encoding for a single image"""
        if not os.path.exists(image_path):
            return None, "Image file not found."

        try:
            # Load image and convert to RGB
            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect face bounding boxes, then encode
            boxes = face_recognition.face_locations(rgb_image, model="hog")
            encodings = face_recognition.face_encodings(rgb_image, boxes)

            if not encodings:
                return None, "No face detected in the reference image."
            
            # Return the first encoding found
            return encodings[0], "Encoding generated successfully."
        except Exception as e:
            return None, f"Error during encoding: {str(e)}"

    def encode_faces(self):
        """Legacy batch method - now primarily handles cloud sync logic if needed"""
        return False, "Batch encoding is deprecated. Use cloud enrollment instead."
