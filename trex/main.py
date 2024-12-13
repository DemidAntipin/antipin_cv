import cv2
import numpy
import time
import mss
import pyautogui
#cv2.namedWindow("Window",cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Window",600, 120)
sct = mss.mss()
time.sleep(5) # время на открыть игру после запуска программы
speed_px=8 # примерная изначальная скорость пикселей в сек.
speed=1 # множитель скорости относительно изначальной
score=0 # примерное кол-во очков, в идеале - полностью синхронизовано с очками в игре
bbox = {"top": 225, "left": 650, "width": 600, "height": 150} # параметры окна игры
prev_time=time.time() # время предыдущего кадра
jumped=False # дино в прыжке
while True:
    img =numpy.asarray(sct.grab(bbox))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)[1]
    mask=cv2.bitwise_not(thresh)
    mask=cv2.erode(mask, None, iterations=1) # убрать землю, оставляя только объекты
    mask=cv2.dilate(mask,None,iterations=5) # объединить рядом стоящие кактусы в 1 объект
    score+=(time.time()-prev_time)*speed_px*speed # примерная формула подсчета очков, не идеальная
    prev_time=time.time()
    if score < 1000:
        speed=(speed_px+0.5*(score//100))/8 # примерная формула скорости игры при ускорении каждые 100 очков
    else:
        speed=(speed_px+(5+0.5*((score-1000)//200)))/8 # примерная формула скорости игры при ускорении каждые 200 очков (после 1000)
    conts,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cont in conts:
        (x, y, w, h)=cv2.boundingRect(cont)
        if (x<30 or y+h<=96): # не учитывать динозаврика, перепрыгнутые объекты и высоких птиц (под которыми можно пробежать)
            continue
        #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 3) #обвод преград для отладки
        if x+w*0.75+h*0.75<200*speed**0.75: # примерная формула расчёта расстояния до прыжка
            if jumped and x+w+h*0.1<70*speed**1.1: # примерный расчёт, чтобы приземлиться сразу за препятствием, чтобы быть готовым к новому прыжку
                pyautogui.keyDown("down")
                pyautogui.keyUp("down")
                jumped=False
            else:
                pyautogui.keyDown("space")
                jumped=True
    #cv2.imshow("Window", img)
    key=cv2.waitKey(1)
    if key == ord('q'):
        break
cv2.destroyAllWindows()