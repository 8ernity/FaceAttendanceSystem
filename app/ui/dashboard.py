import customtkinter as ctk
import threading
import cv2
from PIL import Image
import os
import pandas as pd
from datetime import datetime
from app.utils.helpers import ATTENDANCE_DIR

def _build_home_page(self):
    f = ctk.CTkFrame(self.main_container, fg_color="transparent")
    self.frames["home"] = f

    title = ctk.CTkLabel(f, text="Overview Dashboard", font=ctk.CTkFont(family="Inter", size=26, weight="bold"), text_color="#ffffff")
    title.pack(pady=(30, 10), anchor="w", padx=30)

    # Top Stats Cards
    stats_frame = ctk.CTkFrame(f, fg_color="transparent")
    stats_frame.pack(fill="x", pady=(10, 20), padx=20)

    self.stat_vars = {}
    cards_info = [
        ("👥 Total Users", "0", "All enrolled identities", "#00e5ff"), 
        ("🟢 Present", "0", "Updated just now", "#00e676"), 
        ("🔴 Absent", "0", "Action required", "#ff5252"), 
        ("✨ Accuracy", "98.5%", "↑ 1.2% vs last week", "#7c4dff")
    ]
    for i, (title_text, val, sub_text, color) in enumerate(cards_info):
        stats_frame.grid_columnconfigure(i, weight=1)
        card = ctk.CTkFrame(stats_frame, fg_color="#1a1d24", corner_radius=12, border_width=1, border_color="#2a2a2a")
        card.grid(row=0, column=i, padx=10, sticky="ew")

        ctk.CTkLabel(card, text=title_text, font=ctk.CTkFont(family="Inter", size=13, weight="bold"), text_color="#94a1b2").pack(pady=(15, 0), anchor="w", padx=20)
        lbl = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(family="Inter", size=32, weight="bold"), text_color=color)
        lbl.pack(pady=(5, 0), anchor="w", padx=20)
        ctk.CTkLabel(card, text=sub_text, font=ctk.CTkFont(family="Inter", size=11), text_color="#5a6575").pack(pady=(0, 15), anchor="w", padx=20)
        self.stat_vars[i] = lbl

    # Middle Section: Recent Detections
    mid_frame = ctk.CTkFrame(f, fg_color="#1a1d24", corner_radius=12, border_width=1, border_color="#2a2a2a")
    mid_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    mid_title = ctk.CTkLabel(mid_frame, text="Latest System Detections", font=ctk.CTkFont(family="Inter", size=14, weight="bold"), text_color="#ffffff")
    mid_title.pack(anchor="w", padx=20, pady=(15, 10))

    self.home_recent_log = ctk.CTkScrollableFrame(mid_frame, fg_color="transparent")
    self.home_recent_log.pack(fill="both", expand=True, padx=10, pady=10)