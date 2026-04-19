import customtkinter as ctk
import threading
import cv2
from PIL import Image
import os
import pandas as pd
from datetime import datetime
from app.utils.helpers import ATTENDANCE_DIR

def _build_right_sidebar(self):
    self.right_sidebar = ctk.CTkFrame(self, width=320, corner_radius=15, fg_color="#13151a", border_width=1, border_color="#2a2a2a")
    self.right_sidebar.grid(row=0, column=2, padx=(10, 20), pady=20, sticky="nsew")
    self.right_sidebar.grid_rowconfigure(1, weight=1) # Log area expands
    self.right_sidebar.grid_columnconfigure(0, weight=1)

    # --- Section 1: Attendance Overview Card ---
    overview_card = ctk.CTkFrame(self.right_sidebar, fg_color="#1a1d24", corner_radius=12, border_width=1, border_color="#2a2a2a")
    overview_card.grid(row=0, column=0, sticky="nsew", padx=15, pady=(20, 10))

    title1 = ctk.CTkLabel(overview_card, text="ATTENDANCE OVERVIEW", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#94a1b2")
    title1.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))

    stats_frame = ctk.CTkFrame(overview_card, fg_color="transparent")
    stats_frame.grid(row=1, column=0, sticky="nw", padx=15, pady=(0, 15))

    self.lbl_present = ctk.CTkLabel(stats_frame, text="🟢 Present: 0", font=ctk.CTkFont(family="Inter", size=13), text_color="#ffffff")
    self.lbl_present.grid(row=0, column=0, sticky="w", pady=(0, 5))
    self.lbl_absent = ctk.CTkLabel(stats_frame, text="🔴 Absent:  0", font=ctk.CTkFont(family="Inter", size=13), text_color="#ffffff")
    self.lbl_absent.grid(row=1, column=0, sticky="w", pady=(0, 5))
    self.lbl_total = ctk.CTkLabel(stats_frame, text="⚪ Total:     0", font=ctk.CTkFont(family="Inter", size=13), text_color="#ffffff")
    self.lbl_total.grid(row=2, column=0, sticky="w")

    canvas_bg = "#1a1d24"
    self.progress_canvas = ctk.CTkCanvas(overview_card, width=80, height=80, bg=canvas_bg, highlightthickness=0)
    self.progress_canvas.grid(row=1, column=1, sticky="e", padx=(10, 15), pady=(0, 15))
    self._draw_progress(0)

    # --- Section 2: Recent Activity Card ---
    log_card = ctk.CTkFrame(self.right_sidebar, fg_color="#1a1d24", corner_radius=12, border_width=1, border_color="#2a2a2a")
    log_card.grid(row=1, column=0, sticky="nsew", padx=15, pady=(10, 20))
    log_card.grid_rowconfigure(1, weight=1)
    log_card.grid_columnconfigure(0, weight=1)

    title2 = ctk.CTkLabel(log_card, text="RECENT ACTIVITY", font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#94a1b2")
    title2.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))

    self.log_scrollable = ctk.CTkScrollableFrame(log_card, fg_color="transparent")
    self.log_scrollable.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 10))
    self.log_scrollable.grid_columnconfigure(0, weight=1)

    self.last_log_count = -1

def _draw_progress(self, percentage):
    self.progress_canvas.delete("all")
    self.progress_canvas.create_arc(5, 5, 75, 75, start=0, extent=359.9, outline="#2a2a2a", width=6, style="arc")
    extent = -(percentage / 100.0) * 359.9
    self.progress_canvas.create_arc(5, 5, 75, 75, start=90, extent=extent, outline="#00e5ff", width=6, style="arc")
    self.progress_canvas.create_text(40, 40, text=f"{int(percentage)}%", fill="#00e5ff", font=("Inter", 13, "bold"))

def update_right_sidebar(self):
    try:
        users_data = self.cloud_manager.fetch_all_users()
        total_users = len(users_data["names"]) if users_data else 0

        today = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(ATTENDANCE_DIR, f"Attendance_{today}.csv")

        present_count = 0
        df = None
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            present_count = len(df)

        absent_count = max(0, total_users - present_count)
        percentage = (present_count / total_users * 100) if total_users > 0 else 0

        self.lbl_present.configure(text=f"🟢 Present: {present_count}")
        self.lbl_absent.configure(text=f"🔴 Absent:  {absent_count}")
        self.lbl_total.configure(text=f"⚪ Total:     {total_users}")

        if hasattr(self, 'stat_vars'):
            self.stat_vars[0].configure(text=str(total_users))
            self.stat_vars[1].configure(text=str(present_count))
            self.stat_vars[2].configure(text=str(absent_count))

        self._draw_progress(percentage)

        if df is not None and len(df) != self.last_log_count:
            self.last_log_count = len(df)

            for widget in self.log_scrollable.winfo_children():
                widget.destroy()
            if hasattr(self, 'home_recent_log'):
                for widget in self.home_recent_log.winfo_children():
                    widget.destroy()

            df_reversed = df.iloc[::-1]

            for idx, row in df_reversed.iterrows():
                # --- Sidebar Log Item ---
                item_frame = ctk.CTkFrame(self.log_scrollable, fg_color="transparent")
                item_frame.pack(fill="x", pady=2, padx=5)
                item_frame.grid_columnconfigure(1, weight=1)

                ctk.CTkLabel(item_frame, text="👤", font=ctk.CTkFont(size=18)).grid(row=0, column=0, rowspan=2, padx=(5, 10), pady=5)

                ctk.CTkLabel(item_frame, text=row['Name'], font=ctk.CTkFont(family="Inter", size=13, weight="bold"), text_color="#ffffff").grid(row=0, column=1, sticky="w", pady=(5, 0))

                status_color = "#00e676" if row['Status'] == "Present" else "#ff5252"
                status_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                status_frame.grid(row=1, column=1, sticky="w", pady=(0, 5))
                ctk.CTkLabel(status_frame, text=row['Status'], font=ctk.CTkFont(family="Inter", size=11, weight="bold"), text_color=status_color).pack(side="left")
                ctk.CTkLabel(status_frame, text=f"({row['Time'][:5]})", font=ctk.CTkFont(family="Inter", size=11), text_color="#94a1b2").pack(side="left", padx=(5, 0))

                # --- Home Page Log Item ---
                if hasattr(self, 'home_recent_log') and idx >= len(df) - 10:
                    row_bg = "#1a1d24" if idx % 2 == 0 else "#15171d"
                    home_item = ctk.CTkFrame(self.home_recent_log, fg_color=row_bg, corner_radius=8)
                    home_item.pack(fill="x", pady=2, padx=5)
                    home_item.grid_columnconfigure((0,1,2,3), weight=1)

                    ctk.CTkLabel(home_item, text=f"👤  {row['Name']}", font=ctk.CTkFont(family="Inter", size=14, weight="bold"), text_color="#ffffff").grid(row=0, column=0, pady=12, padx=20, sticky="w")
                    ctk.CTkLabel(home_item, text=row['Date'], font=ctk.CTkFont(family="Inter", size=13), text_color="#94a1b2").grid(row=0, column=1, sticky="w")
                    ctk.CTkLabel(home_item, text=row['Time'], font=ctk.CTkFont(family="Inter", size=13), text_color="#94a1b2").grid(row=0, column=2, sticky="w")

                    badge = ctk.CTkFrame(home_item, fg_color=status_color, corner_radius=12)
                    badge.grid(row=0, column=3, sticky="e", padx=20)
                    ctk.CTkLabel(badge, text=row['Status'], font=ctk.CTkFont(family="Inter", size=11, weight="bold"), text_color="#ffffff").pack(padx=12, pady=2)

    except Exception as e:
        print(f"Sidebar update error: {e}")

    self.after(2000, self.update_right_sidebar)