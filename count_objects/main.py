import zmq
import cv2
import numpy as np
context=zmq.Context()
socket=context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5555
socket.connect("tcp://192.168.0.100:%s" % port)
cv2.namedWindow("Client recv", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

lower=(0, 70, 0)
upper=(255, 255, 255)

while True:
    msg=socket.recv()
    frame=cv2.imdecode(np.frombuffer(msg, np.uint8), -1)
    key=cv2.waitKey(100)
    if key==ord('q'):
        break
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv, lower, upper)
    mask=cv2.erode(mask, None, iterations=4)
    mask=cv2.dilate(mask, None, iterations=4)
    cv2.imshow("Mask", mask)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    count_cubes=0
    count_spheres=0
    for i,cnt in enumerate(cnts):
        area=cv2.contourArea(cnt)
        if area < 1000:
            continue
        (x,y), r = cv2.minEnclosingCircle(cnt)
        _, (w,h), _ = cv2.minAreaRect(cnt)
        if area/h/w>0.8:
            count_cubes+=1
        else:
            count_spheres+=1
        cv2.circle(frame, (int(x), int(y)), int(r), (0,0,255), 5)
    cv2.putText(frame,f"Cubes {count_cubes}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255 ,255))
    cv2.putText(frame,f"Spheres {count_spheres}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255 ,255))
    cv2.imshow("Client recv", frame)
