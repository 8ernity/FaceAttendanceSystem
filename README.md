# FaceTracker AI - Smart Attendance System

A complete, production-ready AI-Based Attendance System built using OpenCV, `face_recognition`, and a modern `CustomTkinter` UI.

## Features Added

*   **Modular Architecture**: Splitted core features into robust modules (`dataset`, `encoding`, `recognizer`, `logger`).
*   **Built-in Dataset Creation**: Register via camera, automatically tracks and saves images.
*   **Deep Learning Encodings**: Uses dlib's HOG/CNN via `face_recognition` to build unique signature encodings.
*   **Advanced Recognition**:
    *   Rejects poorly matched faces as **Unknown**.
    *   Uses a **Confidence Score (%)** to measure how close a face is tracking.
*   **Robust CSV Analytics**: Logs Date, Time, and entry status. Automatically debounces entries preventing duplicates for the same user right away!
*   **Beautiful UI**: Constructed with CustomTkinter for a responsive, clean, and glassmorphic aesthetic.
*   **Audio Alerts**: Generates distinct system beeps when attendance passes or when an unknown face attempts to pass!

## Prerequisites

Be sure you have visual C++ build tools installed for `dlib` (used implicitly by face_recognition) or use a pre-built wheel if on Windows!

```bash
pip install -r requirements.txt
```

## How to Run

Simply execute the main entrypoint. The necessary folders (`data/dataset`, `data/encodings`, `data/attendance`) are built automatically!

```bash
python main.py
```

## Preview 
Your attendance will be logged to `data/attendance/Attendance_YYYY-MM-DD.csv` in the format:

| Name       | Date       | Time     | Status  |
| ---        | ---        | ---      | ---     |
| John Doe   | 2026-04-18 | 08:34:20 | Present |
