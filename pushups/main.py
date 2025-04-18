from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from pathlib import Path
import cv2
import time
import numpy as np

path = Path(__file__).parent
model_path = path / "yolo11n-pose.pt"
model = YOLO(model_path)

def distance(p1, p2):
    return ((int(p1[0]) - int(p2[0]))**2 + (int(p1[1]) - int(p2[1]))**2)**0.5

def angle(a, b, c):
    d = np.arctan2(c[1] - b[1], c[0] - b[0])
    e = np.arctan2(a[1] - b[1], a[0] - b[0])
    ang = np.rad2deg(d - e)
    ang = ang + 360 if ang < 0 else ang
    return 360 - ang if ang > 180 else ang

def process(image, keypoints):
    lshoulder = keypoints[5]
    rshoulder = keypoints[6]
    lelbow = keypoints[7]
    relbow = keypoints[8]
    lwrist = keypoints[9]
    rwrist = keypoints[10]

    try:
        angle_left = angle(lshoulder, lelbow, lwrist)
        angle_right = angle(rshoulder, relbow, rwrist)
        x, y = int(lelbow[0]) + 10, int(lelbow[1]) + 10
        cv2.putText(image, f"Left Elbow Angle: {angle_left:.1f}", (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (25, 25, 255), 2)

        x, y = int(relbow[0]) + 10, int(relbow[1]) + 30
        cv2.putText(image, f"Right Elbow Angle: {angle_right:.1f}", (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (25, 25, 255), 2)

        return angle_left, angle_right
    except ZeroDivisionError:
        pass
    return None, None

cap = cv2.VideoCapture("http://192.168.91.113:4747/video")
last_time = time.time()
last_push_up = time.time()
flag = False
count = 0
writer = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*"avc1"), 10, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    curr_time = time.time()
    cv2.putText(frame, f"FPS: {1 / (curr_time - last_time):.1f}", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (25, 255, 25), 1)
    last_time = curr_time
    results = model(frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if not results:
        continue
    result = results[0]
    keypoints = result.keypoints.xy.tolist()
    if not keypoints:
        continue
    keypoints = keypoints[0]
    if not keypoints:
        continue
    annotator = Annotator(frame)
    annotator.kpts(result.keypoints.data[0], result.orig_shape, 5, True)
    annotated = annotator.result()
    angle_left, angle_right = process(annotated, keypoints)
    if flag and (angle_left < 140 and angle_right < 140):
        count += 1
        last_push_up = time.time()
        flag = False
    elif angle_left > 140 and angle_right > 140:
        flag = True

    cv2.putText(frame, f"Count: {count}", (30, 40), cv2.FONT_HERSHEY_PLAIN, 1.5, (25, 255, 25), 1)
    cv2.imshow("Pose", annotated)
    if curr_time - last_push_up>20:
        count=0
    cv2.imshow("YOLO", frame)
    writer.write(frame)

writer.release()
cap.release()
cv2.destroyAllWindows()