import cv2

file="balls_and_rects.png"

img = cv2.imread(file, cv2.IMREAD_COLOR)

hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh=cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

rects={}
circles={}

for cnt in cnts:
    area=cv2.contourArea(cnt)
    [_,_,w,h]=cv2.boundingRect(cnt)
    (x,y), _ = cv2.minEnclosingCircle(cnt)
    color=hsv[int(y),int(x)][0]
    if w*h/area<1.2:
        if color in rects:
            rects[color]+=1
        else:
            rects[color]=1
    else:
        if color in circles:
            circles[color]+=1
        else:
            circles[color]=1

for i in rects.items():
    print(f"Прямоугольников с оттенком {i[0]}: {i[1]}")
print(f"Всего прямоугольников: {sum(rects.values())}")
for i in circles.items():
    print(f"Кругов с оттенком {i[0]}: {i[1]}")
print(f"Всего кругов: {sum(circles.values())}")