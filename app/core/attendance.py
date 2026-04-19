import os
import pandas as pd
from datetime import datetime
from app.utils.helpers import ATTENDANCE_DIR, play_alert

class AttendanceLogger:
    def __init__(self):
        self.filepath = ""
        self._set_today_file()

    def _set_today_file(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.filepath = os.path.join(ATTENDANCE_DIR, f"Attendance_{today}.csv")
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
            df.to_csv(self.filepath, index=False)

    def mark_attendance(self, name):
        self._set_today_file() # Ensure filename is up-to-date across midnight

        if name == "Unknown":
            return False, "Unknown face detected."

        try:
            df = pd.read_csv(self.filepath)
            
            # Check if already marked today
            if name in df["Name"].values:
                return False, f"[*] Attendance already marked for {name}"

            # Mark attendance
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")

            new_record = pd.DataFrame([{"Name": name, "Date": date_str, "Time": time_str, "Status": "Present"}])
            df = pd.concat([df, new_record], ignore_index=True)
            df.to_csv(self.filepath, index=False)
            
            # Visual or sound alert
            play_alert(success=True)
            
            return True, f"[+] Successfully recorded attendance for {name} at {time_str}"
            
        except Exception as e:
            return False, f"[-] File Error: {e}"
