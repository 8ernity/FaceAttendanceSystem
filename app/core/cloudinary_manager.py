import os
import cloudinary
import cloudinary.uploader
import numpy as np
import json

class CloudinaryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CloudinaryManager, cls).__new__(cls)
            cls._instance._initialized = False
            cls._instance.users_file = os.path.join("data", "users.json")
        return cls._instance

    def initialize(self, cloud_name=None, api_key=None, api_secret=None):
        """Initializes the Cloudinary SDK and Local Storage"""
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)

        # Check if credentials are provided
        if not all([cloud_name, api_key, api_secret]):
            return False, "Cloudinary credentials missing. Please configure them in main.py."

        try:
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret,
                secure=True
            )
            self._initialized = True
            return True, "Cloudinary initialized successfully."
        except Exception as e:
            return False, f"Cloudinary initialization failed: {str(e)}"

    def upload_user(self, name, encoding, image_path=None):
        """Uploads image to Cloudinary and saves encoding to local JSON"""
        try:
            image_url = ""
            if image_path and os.path.exists(image_path):
                # Upload image to Cloudinary
                response = cloudinary.uploader.upload(
                    image_path,
                    folder="face_attendance/users",
                    public_id=name,
                    overwrite=True
                )
                image_url = response.get("secure_url")

            # Save to local JSON (Replacement for Firestore)
            with open(self.users_file, "r") as f:
                users_data = json.load(f)

            users_data[name] = {
                "name": name,
                "encoding": encoding.tolist() if isinstance(encoding, np.ndarray) else encoding,
                "image_url": image_url
            }

            with open(self.users_file, "w") as f:
                json.dump(users_data, f, indent=4)

            return True, f"User {name} successfully saved (Cloudinary + Local DB)."
        except Exception as e:
            return False, f"Failed to save user: {str(e)}"

    def fetch_all_users(self):
        """Fetches all user records from local JSON"""
        try:
            if not os.path.exists(self.users_file):
                return {"names": [], "encodings": []}

            with open(self.users_file, "r") as f:
                users_data = json.load(f)
            
            known_names = []
            known_encodings = []
            
            for name, data in users_data.items():
                known_names.append(name)
                known_encodings.append(np.array(data['encoding']))
            
            return {"names": known_names, "encodings": known_encodings}
        except Exception as e:
            print(f"Error fetching users: {e}")
            return None
