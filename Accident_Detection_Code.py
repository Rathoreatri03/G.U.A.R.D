from ultralytics import YOLO
import cv2
import cvzone
import math


cap = cv2.VideoCapture("Test-1.mp4")

model = YOLO("Accident_Detection_Accuracy_Model.pt")

classNames = ['Accident']

frame_count = 0  # Counter to keep track of frames
while True:
    success, img = cap.read()
    if not success:
        break

    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))

            conf = math.ceil(box.conf[0] * 100) / 100
            cls = int(box.cls[0])
            cvzone.putTextRect(img, f"{classNames[cls]}{conf}", (max(0, x1), max(35, y1)), scale=0.7, thickness=1)

            # Check if accident class is detected
            if classNames[cls] == 'Accident':
                # Save the frame where accident is detected
                frame_count += 1
                cv2.imwrite(f'accident_frame.jpg', img)

                # Activate both functions when accident is detected
                Live_Location(serial_port, baud_rate, sender_email, sender_password, receiver_emails)

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()