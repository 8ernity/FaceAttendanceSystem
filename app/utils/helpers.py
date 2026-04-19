import os
import winsound
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATASET_DIR = os.path.join(DATA_DIR, "dataset")
ENCODINGS_DIR = os.path.join(DATA_DIR, "encodings")
ATTENDANCE_DIR = os.path.join(DATA_DIR, "attendance")

def setup_directories():
    """Ensure all required directories exist."""
    for d in [DATASET_DIR, ENCODINGS_DIR, ATTENDANCE_DIR]:
        os.makedirs(d, exist_ok=True)

def play_alert(success=True):
    """Play a beep sound. High pitch for success, lower string for failure/unknown."""
    try:
        if success:
            winsound.Beep(1200, 200) # Frequency, Duration in ms
        else:
            winsound.Beep(500, 500)
    except:
        pass
