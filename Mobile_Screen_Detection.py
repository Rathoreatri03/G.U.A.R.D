from ultralytics import YOLO
import cv2
import cvzone
import math

cap = cv2.VideoCapture(0)
cap.set(4, 720)
cap.set(3, 1280)

modelM = YOLO("MobileScreenDetection.pt")
modelM2 = YOLO("../Yolo-Wieghts/yolov8n.pt")

classNames_M = ["mobile_screen"]
classNames_M2 = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                 "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                 "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                 "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                 "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                 "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                 "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                 "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                 "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                 "teddy bear", "hair drier", "toothbrush"
                 ]

while True:
    success, img = cap.read()

    # Detection using modelM2
    results_M2 = modelM2(img, stream=True)
    # Detection using modelM
    results_M = modelM(img, stream=True)

    # Combine bounding boxes from both models
    combined_boxes = []

    # Iterate through the results of both models and store bounding boxes
    for r_M2 in results_M2:
        for box in r_M2.boxes:
            if box.conf[0] > 0.1 and classNames_M2[int(box.cls[0])] == "cell phone":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                combined_boxes.append((x1, y1, x2, y2))

    for r_M in results_M:
        for box in r_M.boxes:
            if box.conf[0] > 0.5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Removed the extra closing parenthesis here
                combined_boxes.append((x1, y1, x2, y2))

    # Draw a single bounding box around the combined bounding boxes
    if combined_boxes:
        min_x = min(box[0] for box in combined_boxes)
        min_y = min(box[1] for box in combined_boxes)
        max_x = max(box[2] for box in combined_boxes)
        max_y = max(box[3] for box in combined_boxes)

        cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
