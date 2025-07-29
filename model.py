import cv2
import time
import requests  # To send HTTP requests to ESP32

# ESP32 Server URL (Replace with your ESP32's IP address)
ESP32_IP = "192.168.223.178"  # Replace with your ESP32 IP
ESP32_URL = f"http://{ESP32_IP}/alert"  # URL for the alert route

# Load the pre-trained Haar Cascade Classifiers for face and eye detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
EAR_THRESHOLD = 0.25

# Approximate EAR using the eye rectangle (not using landmarks)
def calculate_ear(eye_points):
    if len(eye_points) < 2:
        return None  # Not enough eyes to calculate EAR
    
    (x1, y1, w1, h1) = eye_points[0]  # First eye
    (x2, y2, w2, h2) = eye_points[1]  # Second eye
    
    ear = (h1 + h2) / (w1 + w2)  # Simplified approximation
    return ear

def is_drowsy(eye_points):
    EAR = calculate_ear(eye_points)
    if EAR is None:
        return False  # Cannot detect EAR, so assume not drowsy
    return EAR < EAR_THRESHOLD

# Function to detect drowsiness
def detect_drowsiness():
    cap = cv2.VideoCapture(0)  # Use default camera (0 for first camera)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        # Check if faces are detected
        if len(faces) == 0:
            print("No faces detected!")
            try:
                # Sending HTTP GET request to ESP32 with 'no_face' message
                response = requests.get(f"{ESP32_URL}?message=no_face")
                print(f"ESP32 Response: {response.text}")
            except Exception as e:
                print(f"Failed to send alert to ESP32: {e}")
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            
            # Detect eyes within the face region
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)

            # Debugging: Print how many eyes are detected
            print(f"Eyes detected: {len(eyes)}")
            
            # If no eyes are detected, print "Eyes closed"
            if len(eyes) == 0:
                print("Eyes closed or not detected!")
                try:
                    # Sending HTTP GET request to ESP32 with 'eyes_closed' message
                    response = requests.get(f"{ESP32_URL}?message=eyes_closed")
                    print(f"ESP32 Response: {response.text}")
                except Exception as e:
                    print(f"Failed to send alert to ESP32: {e}")
            
            # Draw rectangles around detected eyes
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)
            
            # If two eyes are detected, check if the person is drowsy
            if len(eyes) >= 2:
                if is_drowsy(eyes):  # If drowsiness detected
                    print("Drowsiness detected! Sending alert to ESP32...")
                    try:
                        # Sending HTTP GET request to ESP32
                        response = requests.get(f"{ESP32_URL}?message=drowsy")
                        print(f"ESP32 Response: {response.text}")
                    except Exception as e:
                        print(f"Failed to send alert to ESP32: {e}")
                    cap.release()
                    cv2.destroyAllWindows()
                    return True

        # Display the resulting frame
        cv2.imshow('Video Feed', frame)
        
        # Break the loop on pressing the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(1)

    cap.release()
    cv2.destroyAllWindows()

# Call the detection function
drowsy = detect_drowsiness()
if drowsy:
    print("Driver is drowsy! Take necessary action.")