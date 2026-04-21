# 🚀 FaceTracker AI – Smart Attendance System

A modern AI-powered face recognition attendance system built with Python. This project automates attendance marking using real-time facial recognition, offering a clean dashboard UI and efficient data handling.

---

## 📌 Overview

FaceTracker AI is designed to replace traditional attendance systems with an intelligent, automated solution. It uses computer vision and machine learning techniques to detect, recognize, and log user attendance in real-time.

The application features a modern dashboard interface, live camera feed, analytics panel, and structured data management.

---

## ✨ Features

* 🎥 **Real-Time Face Recognition**

  * Detect and recognize faces using OpenCV
  * Displays name and confidence score

* 🧠 **AI-Based Encoding System**

  * Uses face encodings instead of storing multiple images
  * Optimized for performance and storage

* 📊 **Interactive Dashboard**

  * Overview cards (Total Users, Present, Absent, Accuracy)
  * Live system status and updates

* 📝 **Automated Attendance Logging**

  * Records name, date, time, and status
  * Stores logs in structured format (CSV / database)

* 📈 **Analytics Panel**

  * Attendance overview
  * Activity logs
  * Visual indicators

* 👤 **User Enrollment System**

  * Add new users with face capture
  * Train model dynamically

* 🎨 **Modern UI**

  * Dark theme dashboard
  * Sidebar navigation
  * Responsive layout

---

## 🏗️ Project Structure

```plaintext
FaceAttendanceSystem/
│
├── app/
│   ├── core/          # AI logic (face recognition, camera, attendance)
│   ├── ui/            # UI components (dashboard, camera view, records)
│   ├── utils/         # Helper functions and constants
│   └── main_app.py    # Main application controller
│
├── data/
│   ├── images/        # Captured user images
│   ├── encodings/     # Stored face encodings
│   └── attendance.csv # Attendance logs
│
├── assets/            # Icons, styles, UI resources
├── run.py             # Entry point
├── requirements.txt   # Dependencies
└── README.md
```

---

## ⚙️ Tech Stack

* **Language:** Python
* **Libraries:**

  * OpenCV (Computer Vision)
  * face_recognition (Face Encoding & Matching)
  * CustomTkinter (Modern UI)
  * NumPy, Pandas (Data handling)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/FaceAttendanceSystem.git
cd FaceAttendanceSystem
```

---

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the Application

```bash
python run.py
```

---

## 📷 How It Works

1. **Add User**

   * Enter name
   * Capture face data
   * Generate face encoding

2. **Start Live System**

   * Webcam detects faces
   * Matches with stored encodings

3. **Mark Attendance**

   * Logs entry with timestamp
   * Updates dashboard in real-time

---

## 📊 Sample Output

* Recognized Face → Name + Confidence
* Attendance Record →

  ```
  Name | Date | Time | Status
  ```

---

## 🔐 Optimization Strategy

* Stores **face encodings instead of raw images**
* Reduces storage usage significantly
* Improves recognition speed

---

## 🌐 Future Enhancements

* ☁️ Cloud integration (Firebase / AWS S3)
* 📱 Mobile app version
* 📊 Advanced analytics dashboard
* 🔔 Notification system
* 🧑‍🤝‍🧑 Multi-user support with roles

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you like this project

Give it a star on GitHub and share it!

---
