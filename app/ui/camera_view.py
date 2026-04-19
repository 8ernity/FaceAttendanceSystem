import customtkinter as ctk
import threading
import cv2
from PIL import Image
import os
import pandas as pd
from datetime import datetime
from app.utils.helpers import ATTENDANCE_DIR

def _build_recognize_page(self):
    f = ctk.CTkFrame(self.main_container, fg_color="transparent")
    self.frames["recognize"] = f

    title = ctk.CTkLabel(f, text="Live Camera System", font=ctk.CTkFont(family="Inter", size=26, weight="bold"), text_color="#ffffff")
    title.pack(pady=(30, 10), anchor="w", padx=30)

    ctrl_frame = ctk.CTkFrame(f, fg_color="transparent")
    ctrl_frame.pack(fill="x", pady=(0, 10), padx=30)

    self.start_btn = ctk.CTkButton(ctrl_frame, text="▶ Start Scanner", 
                                   command=self.start_attendance, height=40, width=140, 
                                   font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                                   fg_color="#00c853", hover_color="#00e676", corner_radius=8)
    self.start_btn.pack(side="left", padx=(0, 15))

    self.stop_btn = ctk.CTkButton(ctrl_frame, text="■ Stop Scanner", 
                                  command=self.stop_attendance, height=40, width=140, 
                                  font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                                  fg_color="#ff5252", hover_color="#ff1744", corner_radius=8)
    self.stop_btn.pack(side="left")
    self.stop_btn.configure(state="disabled")

    # Video container
    video_wrapper = ctk.CTkFrame(f, fg_color="#1a1d24", corner_radius=12, border_width=1, border_color="#2a2a2a")
    video_wrapper.pack(expand=True, fill="both", padx=30, pady=(0, 30))

    # Top bar in video wrapper
    cam_top_bar = ctk.CTkFrame(video_wrapper, fg_color="transparent", height=40)
    cam_top_bar.pack(fill="x", padx=15, pady=10)
    self.cam_live_indicator = ctk.CTkLabel(cam_top_bar, text="⚫ OFFLINE", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#5a6575")
    self.cam_live_indicator.pack(side="left")

    self.video_label = ctk.CTkLabel(video_wrapper, text="Camera Idle", text_color="#5a6575", font=ctk.CTkFont(family="Inter", size=16))
    self.video_label.pack(expand=True, fill="both", padx=10, pady=(0,10))