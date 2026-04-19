import customtkinter as ctk
import threading
import cv2
from PIL import Image
import os
import pandas as pd
from datetime import datetime
from app.utils.helpers import ATTENDANCE_DIR

def _build_add_user_page(self):
    f = ctk.CTkFrame(self.main_container, fg_color="transparent")
    self.frames["add"] = f

    title = ctk.CTkLabel(f, text="Enroll New Identity", font=ctk.CTkFont(family="Inter", size=26, weight="bold"), text_color="#ffffff")
    title.pack(pady=(30, 20), anchor="w", padx=40)

    card = ctk.CTkFrame(f, corner_radius=12, fg_color="#1a1d24", border_width=1, border_color="#2a2a2a")
    card.pack(pady=(0, 20), padx=40, fill="both", expand=True)

    ctk.CTkLabel(card, text="Full Name", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#94a1b2").pack(pady=(30, 5), anchor="w", padx=40)

    self.name_entry = ctk.CTkEntry(card, placeholder_text="e.g. John Doe", 
                                   width=400, height=45, font=ctk.CTkFont(family="Inter", size=14),
                                   fg_color="#0f1115", border_color="#2a2a2a", border_width=1, corner_radius=8)
    self.name_entry.pack(pady=(0, 20), anchor="w", padx=40)

    self.capture_btn = ctk.CTkButton(card, text="✨ Start Data Capture & Train Model", 
                                     width=400, height=45, font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
                                     fg_color="#7c4dff", hover_color="#651fff", corner_radius=8,
                                     command=self.start_capture)
    self.capture_btn.pack(pady=10, anchor="w", padx=40)

    self.add_status_lbl = ctk.CTkLabel(card, text="Waiting for input...", font=ctk.CTkFont(family="Inter", size=12), text_color="#5a6575")
    self.add_status_lbl.pack(pady=(10, 5), anchor="w", padx=40)

    self.add_log = ctk.CTkTextbox(card, width=600, height=180, state="disabled", 
                                  fg_color="#0f1115", border_color="#2a2a2a", border_width=1, corner_radius=8,
                                  text_color="#00e5ff", font=ctk.CTkFont(family="Courier", size=12))
    self.add_log.pack(pady=(0, 30), anchor="w", padx=40)

def start_capture(self):
    name = self.name_entry.get().strip()
    if not name:
        self.log_add_msg("ERROR: Identity name cannot be empty.")
        return

    self.capture_btn.configure(state="disabled")
    self.add_log.configure(state="normal")
    self.add_log.delete("1.0", "end")
    self.add_log.configure(state="disabled")
    self.add_status_lbl.configure(text="Initializing capture...", text_color="#00e5ff")

    def capture_task():
        ref_img_path = ""
        for success, msg in self.dataset_manager.capture_images(name):
            self.log_add_msg(msg)
            if not success:
                break
            if "Reference image captured" in msg:
                ref_img_path = os.path.join(self.dataset_manager.dataset_dir, name, f"{name}_reference.jpg")

        if not ref_img_path:
            self.log_add_msg("ERROR: Failed to capture reference image.")
            self.capture_btn.configure(state="normal")
            self.add_status_lbl.configure(text="Capture failed.", text_color="#ff5252")
            return

        self.log_add_msg("Encoding faces...")
        encoding, msg = self.encoder.generate_encoding(ref_img_path)
        if encoding is None:
            self.log_add_msg(f"ERROR: {msg}")
            self.capture_btn.configure(state="normal")
            self.add_status_lbl.configure(text="Encoding failed.", text_color="#ff5252")
            return

        self.log_add_msg("Syncing with Cloudinary...")
        if not self.cloud_manager._initialized:
            self.log_add_msg("ERROR: Cloudinary not configured. Check main.py.")
            self.capture_btn.configure(state="normal")
            self.add_status_lbl.configure(text="Sync failed.", text_color="#ff5252")
            return

        success, cloud_msg = self.cloud_manager.upload_user(name, encoding, ref_img_path)
        self.log_add_msg(cloud_msg)

        if success:
            self.log_add_msg("SUCCESS: User enrolled successfully.")
            self.add_status_lbl.configure(text="Identity Enrolled Successfully!", text_color="#00e676")
            try:
                import shutil
                shutil.rmtree(os.path.join(self.dataset_manager.dataset_dir, name))
                self.log_add_msg("Cleaned up local storage.")
            except:
                pass
        else:
            self.log_add_msg(f"ERROR: {cloud_msg}")
            self.add_status_lbl.configure(text="Upload failed.", text_color="#ff5252")

        self.capture_btn.configure(state="normal")
        self.name_entry.delete(0, 'end')

    threading.Thread(target=capture_task, daemon=True).start()

def log_add_msg(self, msg):
    self.add_log.configure(state="normal")
    self.add_log.insert("end", "> " + msg + "\n")
    self.add_log.see("end")
    self.add_log.configure(state="disabled")
    self.add_status_lbl.configure(text=msg)