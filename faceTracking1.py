import cv2
from pythonosc import udp_client
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import time

# UDP client (sends data to another app)
client = udp_client.SimpleUDPClient("127.0.0.1", 9999)


model_path = hf_hub_download(
    repo_id="arnabdhar/YOLOv8-Face-Detection",
    filename="model.pt"
)

model = YOLO(model_path)
cap = cv2.VideoCapture(0)

last_send = 0
send_interval = 0.1  # throttle to avoid spamming UDP

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    results = model(frame, verbose=False)

    # Default values (no face)
    face_x = 0.5
    face_y = 0.5
    is_face = 0

    # Process detections (we only take the first face)
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            # Draw the face box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Find center of face
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            # Normalize 0–1
            face_x = cx / w
            face_y = cy / h

            is_face = 1
            break  # Only one face needed

    # Throttle UDP messages
    now = time.time()
    if now - last_send >= send_interval:
        client.send_message("/pose", [face_x, face_y, is_face])
        last_send = now

    cv2.putText(frame, f"Face: {is_face}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Face Tracker", frame)
    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
