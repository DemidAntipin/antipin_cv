from ultralytics import YOLO
from pathlib import Path
import cv2
import time

path=Path(__file__).parent
model_path=path/"best.pt"
model=YOLO(model_path)

cap=cv2.VideoCapture(0)
state="idle"
prev_time=0
cur_time=0
player1_hand=""
player2_hand=""
timer=5
game_result=-1
image=cv2.imread("scirock.jpg")
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("Camera", frame)
    cv2.putText(frame, f"{state} - {timer:.1f}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    results=model(frame)
    result=results[0]
    #anno_frame=results[0].plot()
    if len(result.boxes.xyxy) == 2:
        labels=[]
        for i, box in enumerate(result.boxes.xyxy):
            x1, y1, x2, y2 = box.numpy().astype("int")
            labels.append(result.names[result.boxes.cls[i].item()].lower())
            cv2.rectangle(frame, (x1,y1), (x2, y2), (0, 255, 0), 4)
            cv2.putText(frame, f"{labels[-1]}", (x1+20, y1+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        player1_hand, player2_hand = labels
        if (player1_hand=="rock" and player2_hand=="rock" and state=="idle"):
            state="wait"
            prev_time=time.time()
        if (game_result>=0):
            win_message=['Player 1 win', 'Draw', 'Player 2 Win'][game_result]
            cv2.putText(frame, win_message, (x1+10, y1+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    if (state == "wait"):
        timer -= round(time.time() - prev_time,1)
        prev_time=time.time()
    if (timer<=0):
        timer=0
        if (state=="wait"):
            state="result"
            if player1_hand==player2_hand:
                game_result=1
            elif ((player1_hand=="scissors" and player2_hand=="rock") or (player1_hand=="rock" and player2_hand=="paper") or (player1_hand=="paper" and player2_hand=="scissors")):
                game_result=2
            else:
                game_result=0
            prev_time=time.time()
        if (time.time()-prev_time>10):
            state='idle'
            timer=5
    cv2.imshow("YOLO", frame)
    key=cv2.waitKey(1)
    if key==ord('q'):
        break
    if key==ord('c'):
        state='idle'
        timer=5
cap.release()
cv2.destroyAllWindows()
