# Driver Drowsiness Detection System using OpenCV, ESP32, and Firebase

This project detects driver drowsiness using computer vision and sends real-time alerts to an ESP32 microcontroller, which logs the alerts to Firebase.

## Overview

The system uses a webcam to:
- Detect faces and eyes using Haar cascades
- Estimate drowsiness based on Eye Aspect Ratio (EAR)
- Send alerts to ESP32 via HTTP
- Log alerts to Firebase Realtime Database

## Project Structure

driver_drowsiness_detection/
├── model.py # Python code for detecting drowsiness
├── esp32_alert_handler.ino # ESP32 Arduino code for receiving alerts and sending to Firebase
├── haarcascade_frontalface_default.xml # XML model for face detection
├── haarcascade_eye.xml # XML model for eye detection


## How It Works

1. `model.py` uses OpenCV to capture webcam frames.
2. Haar cascades detect faces and eyes.
3. If:
   - No face is detected → sends `no_face` alert
   - No eyes are detected → sends `eyes_closed` alert
   - EAR is low → sends `drowsy` alert
4. ESP32 receives the alert and stores it in Firebase with a timestamp

## Requirements

### Python (PC side)
- Python 3.x
- OpenCV (`pip install opencv-python`)
- requests

### ESP32 (Microcontroller)
- ESP32 board
- Arduino IDE
- Libraries:
  - Firebase_ESP_Client
  - WiFi
  - WebServer

### Firebase
- Realtime Database setup
- Get:
  - Database URL
  - Legacy Authentication Token

## Setup Instructions

### 1. Python (PC)
- Place the `.xml` files in the same directory as `model.py`
- Run the script:
```bash
python model.py
