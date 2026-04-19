import os
import threading
import customtkinter as ctk
from PIL import Image
import cv2
import pandas as pd
from datetime import datetime

from app.utils.helpers import setup_directories, ATTENDANCE_DIR
from app.core.camera import DatasetManager
from app.core.encoder import Encoder
from app.core.face_recognition import Recognizer

# Configure CustomTkinter settings to achieve a sleek glassmorphic/modern Dark UI
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


from app.ui.sidebar import _build_right_sidebar, _draw_progress, update_right_sidebar
from app.ui.dashboard import _build_home_page
from app.ui.camera_view import _build_recognize_page
from app.ui.records_view import _build_records_page, load_records
from app.ui.add_user_view import _build_add_user_page, start_capture, log_add_msg


class FaceTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FaceTracker AI - Smart Attendance")
        self.geometry("1300x650")
        self.minsize(1200, 600)

        # Initialize Backend Modules
        setup_directories()
        self.dataset_manager = DatasetManager()
        self.encoder = Encoder()
        self.recognizer = Recognizer()
        
        # Initialize Cloudinary & Local Storage
        from app.core.cloudinary_manager import CloudinaryManager
        self.cloud_manager = CloudinaryManager()
        
        # Cloudinary Credentials (Replace with your own from Cloudinary Console)
        # Sign up for free at https://cloudinary.com/
        CLOUDINARY_CONFIG = {
            "cloud_name": "dxylq3l2l",
            "api_key": "855645532692933",
            "api_secret": "Pi7FaAUcojhekuuQbV5kSU0WEpg"
        }
        
        success, msg = self.cloud_manager.initialize(**CLOUDINARY_CONFIG)
        if not success:
            print(f"Warning: {msg}")

        self._build_ui()

    def _build_ui(self):
        """Construct the layout using Grid System for better responsiveness"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0) # Right Sidebar

        # ================= Sidebar =================
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#13151a")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="⚡ FaceTracker AI", 
                                       font=ctk.CTkFont(family="Inter", size=22, weight="bold"), text_color="#00e5ff")
        self.logo_label.grid(row=0, column=0, padx=25, pady=(35, 40), sticky="w")

        # Navigation Buttons
        nav_opts = [
            ("📊  Dashboard", "home", 1),
            ("👤  Add New User", "add", 2),
            ("📷  Live System", "recognize", 3),
            ("📁  View Records", "records", 4)
        ]

        self.nav_buttons = {}
        for text, name, row in nav_opts:
            btn = ctk.CTkButton(self.sidebar_frame, text=text, height=45, font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
                                command=lambda n=name: self.show_frame(n),
                                fg_color="transparent", text_color="#94a1b2",
                                hover_color="#1a1d24", anchor="w", corner_radius=8)
            btn.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
            self.nav_buttons[name] = btn

        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="● System Ready", 
                                         text_color="#00e676", font=ctk.CTkFont(family="Inter", size=13, weight="bold"))
        self.status_label.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="s")

        # ================= Main Content Container =================
        self.main_container = ctk.CTkFrame(self, corner_radius=20, fg_color="#0f1115")
        self.main_container.grid(row=0, column=1, padx=(20, 10), pady=20, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Build individual view pages
        self._build_home_page()
        self._build_add_user_page()
        self._build_recognize_page()
        self._build_records_page()

        # Build right sidebar
        self._build_right_sidebar()

        self.show_frame("home")
        self.after(2000, self.update_right_sidebar)

    def _update_nav_style(self, selected_name):
        for name, btn in self.nav_buttons.items():
            if name == selected_name:
                btn.configure(fg_color="#1a1d24", text_color="#00e5ff")
            else:
                btn.configure(fg_color="transparent", text_color="#94a1b2")

    # ================= Right Sidebar =================
    
    # _build_right_sidebar imported from app.ui

    # _draw_progress imported from app.ui

    # update_right_sidebar imported from app.ui

    # ================= View Pages =================

    # _build_home_page imported from app.ui

    # _build_add_user_page imported from app.ui

    # _build_recognize_page imported from app.ui

    # _build_records_page imported from app.ui

    # ================= Functionality =================

    def show_frame(self, name):
        if hasattr(self, "recognizer") and self.recognizer.is_running and name != "recognize":
            self.stop_attendance()

        for frame_name, frame in self.frames.items():
            if frame_name == name:
                frame.pack(fill="both", expand=True)
                if name == "records":
                    self.load_records()
            else:
                frame.pack_forget()
                
        self._update_nav_style(name)

    # log_add_msg imported from app.ui

    # start_capture imported from app.ui

    def start_attendance(self):
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="● Camera Active", text_color="#00e5ff")
        self.cam_live_indicator.configure(text="🔴 LIVE", text_color="#ff5252")
        
        def recognition_loop():
            for success, msg, frame in self.recognizer.start_recognition():
                if not getattr(self.recognizer, 'is_running', True):
                    break

                if frame is not None:
                    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2image)
                    w, h = img.size
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
                    
                    self.video_label.configure(image=ctk_img, text="")
                    self.video_label._ctk_image = ctk_img
                else:
                    self.status_label.configure(text=msg, text_color="orange" if not success else "#00e5ff")
                    if not success:
                        self.stop_attendance()
                        break

            self.status_label.configure(text="● System Ready", text_color="#00e676")
            
            empty_img = ctk.CTkImage(Image.new('RGB', (1, 1), color="#1a1d24"), size=(1,1))
            self.video_label.configure(image=empty_img, text="Camera Idle")
            self.video_label._ctk_image = empty_img

        threading.Thread(target=recognition_loop, daemon=True).start()

    def stop_attendance(self):
        self.recognizer.stop()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.cam_live_indicator.configure(text="⚫ OFFLINE", text_color="#5a6575")

    # load_records imported from app.ui

# Bind extracted methods to the class
FaceTrackerApp._build_right_sidebar = _build_right_sidebar
FaceTrackerApp._draw_progress = _draw_progress
FaceTrackerApp.update_right_sidebar = update_right_sidebar
FaceTrackerApp._build_home_page = _build_home_page
FaceTrackerApp._build_recognize_page = _build_recognize_page
FaceTrackerApp._build_records_page = _build_records_page
FaceTrackerApp.load_records = load_records
FaceTrackerApp._build_add_user_page = _build_add_user_page
FaceTrackerApp.start_capture = start_capture
FaceTrackerApp.log_add_msg = log_add_msg

if __name__ == "__main__":
    app = FaceTrackerApp()
    app.mainloop()
