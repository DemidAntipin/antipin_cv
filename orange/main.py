from ultralytics import YOLO
from pathlib import Path
import cv2
import time
import numpy as np
from skimage import draw

path=Path(__file__).parent
model_path=path/"facial_best.pt"
model=YOLO(model_path)

oranges=cv2.imread(str(path/"oranges.png"))
hsv_oranges=cv2.cvtColor(oranges, cv2.COLOR_BGR2HSV)

lower=np.array((10, 240, 200))
upper=np.array((15, 255, 255))

mask = cv2.inRange(hsv_oranges, lower, upper)
mask = cv2.dilate(mask, np.ones((7,7)))
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
sorted_contours = sorted(contours, key=cv2.contourArea)
bbox=cv2.boundingRect(sorted_contours[-1])
m=cv2.moments(sorted_contours[-1])
cx = int(m["m10"]/m["m00"])
cy = int(m["m01"]/m["m00"])

rr, cc= draw.disk((5,5), 5)
struct=np.zeros((11,11), np.uint8)
struct[rr,cc]=1

x,y,w,h=bbox
roi=oranges[y:y+h, x:x+w]

cap=cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    result=model(frame)[0]
    annotated=result.plot()
    masks=result.masks
    if masks is None:
        continue
    global_mask=masks[0].data.numpy()[0, :, :]

    for mask in masks[1:]:
        global_mask+=mask.data.numpy()[0, :, :]

    global_mask=cv2.resize(global_mask, (frame.shape[1], frame.shape[0])).astype('uint8')
    global_mask = cv2.dilate(global_mask, struct.astype('uint8'), iterations=2).reshape(frame.shape[0], frame.shape[1], 1)
    parts=(frame*global_mask).astype("uint8")
    pos=np.where(global_mask>0)
    min_y, max_y=int(np.min(pos[0]) * 0.9), int(np.max(pos[0])*1.1)
    min_x, max_x=int(np.min(pos[1]) * 0.9), int(np.max(pos[1])*1.1)
    global_mask=global_mask[min_y:max_y, min_x:max_x]
    parts=parts[min_y:max_y, min_x:max_x]
    resized_parts = cv2.resize(parts, (w, h))
    resized_mask = cv2.resize(global_mask, (w, h))*255
    inverted_mask=cv2.bitwise_not(resized_mask)
    bg=cv2.bitwise_and(roi, roi, mask=inverted_mask)
    combined=cv2.add(bg, resized_parts)
    cv2.imshow("Image", combined)
    cv2.imshow("Parts", annotated)
    key=cv2.waitKey(1)
    if key==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
