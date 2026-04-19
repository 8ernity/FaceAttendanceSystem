import customtkinter as ctk
import threading
import cv2
from PIL import Image
import os
import pandas as pd
from datetime import datetime
from app.utils.helpers import ATTENDANCE_DIR

def _build_records_page(self):
    f = ctk.CTkFrame(self.main_container, fg_color="transparent")
    self.frames["records"] = f

    title_frame = ctk.CTkFrame(f, fg_color="transparent")
    title_frame.pack(fill="x", pady=(30, 10), padx=30)

    title = ctk.CTkLabel(title_frame, text="Daily Attendance Records", font=ctk.CTkFont(family="Inter", size=26, weight="bold"), text_color="#ffffff")
    title.pack(side="left")

    self.refresh_btn = ctk.CTkButton(title_frame, text="↻ Refresh Data", command=self.load_records, 
                                     width=130, height=35, font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                                     fg_color="#1a1d24", hover_color="#222630", border_width=1, border_color="#7c4dff", corner_radius=8)
    self.refresh_btn.pack(side="right")

    # Table Header
    header_frame = ctk.CTkFrame(f, fg_color="#1a1d24", corner_radius=8, border_width=1, border_color="#2a2a2a")
    header_frame.pack(fill="x", padx=30, pady=(10, 0))
    header_frame.grid_columnconfigure((0,1,2,3), weight=1)

    headers = ["ASSOCIATE NAME", "DATE", "TIMESTAMP", "STATUS"]
    for i, text in enumerate(headers):
        ctk.CTkLabel(header_frame, text=text, font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#94a1b2").grid(row=0, column=i, pady=10, padx=15, sticky="w")

    # Table Body (Scrollable)
    self.records_table = ctk.CTkScrollableFrame(f, fg_color="transparent")
    self.records_table.pack(expand=True, fill="both", padx=25, pady=(5, 30))

def load_records(self):
    for widget in self.records_table.winfo_children():
        widget.destroy()

    today = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(ATTENDANCE_DIR, f"Attendance_{today}.csv")

    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            df_reversed = df.iloc[::-1]

            for idx, row in df_reversed.iterrows():
                row_bg = "#1a1d24" if idx % 2 == 0 else "#15171d"
                row_frame = ctk.CTkFrame(self.records_table, fg_color=row_bg, corner_radius=8)
                row_frame.pack(fill="x", pady=2)
                row_frame.grid_columnconfigure((0,1,2,3), weight=1)

                ctk.CTkLabel(row_frame, text=row['Name'], font=ctk.CTkFont(family="Inter", size=13, weight="bold"), text_color="#ffffff").grid(row=0, column=0, pady=12, padx=15, sticky="w")
                ctk.CTkLabel(row_frame, text=row['Date'], font=ctk.CTkFont(family="Inter", size=13), text_color="#94a1b2").grid(row=0, column=1, sticky="w")
                ctk.CTkLabel(row_frame, text=row['Time'], font=ctk.CTkFont(family="Inter", size=13), text_color="#94a1b2").grid(row=0, column=2, sticky="w")

                status_color = "#00e676" if row['Status'] == "Present" else "#ff5252"
                badge = ctk.CTkFrame(row_frame, fg_color=status_color, corner_radius=12)
                badge.grid(row=0, column=3, sticky="w", padx=10)
                ctk.CTkLabel(badge, text=row['Status'], font=ctk.CTkFont(family="Inter", size=11, weight="bold"), text_color="#ffffff").pack(padx=12, pady=2)

        except Exception as e:
            ctk.CTkLabel(self.records_table, text=f"Error parsing CSV format: {e}", text_color="#ff5252").pack(pady=20)
    else:
        ctk.CTkLabel(self.records_table, text="No attendance records found for today's session.", font=ctk.CTkFont(family="Inter", size=14), text_color="#5a6575").pack(pady=40)