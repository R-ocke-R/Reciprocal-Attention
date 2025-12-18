import cv2
from pythonosc import udp_client
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import time

client = udp_client.SimpleUDPClient("127.0.0.1", 9999)
model_path = hf_hub_download(
    repo_id="arnabdhar/YOLOv8-Face-Detection",
    filename="model.pt"
)
model = YOLO(model_path)



eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

cap = cv2.VideoCapture(0)
last_send = 0
send_interval = 1

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    results = model(frame, verbose=False)
    face_x = 0.5
    face_y = 0.5
    face_found = 0

    eye_score = 0.0      
    eye_flag = 0           

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            face_x = cx / w
            face_y = cy / h
            face_found = 1
            face_roi = frame[y1:y2, x1:x2]
            gray_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

            eyes = eye_cascade.detectMultiScale(
                gray_roi,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(20, 20)
            )

            visible_eyes = min(len(eyes), 2)

            # Score: 0 → 0.5 → 1.0
            eye_score = visible_eyes / 2.0

            # Flag: only full score = looking at screen
            eye_flag = 1 if eye_score == 1.0 else 0

            # Draw eyes
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (x1+ex, y1+ey),
                              (x1+ex+ew, y1+ey+eh), (255,0,0), 1)

            break

    # Display info
    cv2.putText(frame, f"EyeScore: {eye_score:.1f}   Flag: {eye_flag}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0,255,0) if eye_flag == 1 else (0,0,255), 2)

    now = time.time()
    if now - last_send >= send_interval:
        client.send_message("/pose",
            [face_x, face_y, eye_flag]
        )
        last_send = now
    cv2.imshow("Face + Eye Tracker", frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
