import cv2
import numpy as np

video_path = 'output.avi'

camera = cv2.VideoCapture(video_path)

cv2.namedWindow("Window",cv2.WINDOW_NORMAL)

prev_frame = None

counter = 0
while True:
    ret, frame = camera.read()

    if not ret:
        break  # Выход из цикла, если кадры закончились

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if prev_frame is not None:
        diff = cv2.absdiff(gray, prev_frame)
        if np.max(diff)==0: # кадр в видео не успел смениться
            continue # этот кадр уже был обработан

    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    thresh=cv2.bitwise_not(thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if (len(contours)==31): # На моём изображении 31 контур, для достоверности можно добавить проверку hierarchy, но в данной задаче она не требуется, в остальных картинках при моей бинаризации другое число контуров
        counter+=1 
    #    cv2.imshow('Window', frame) # проверка картинки, при правильном определении - моя цветная, остальные в серых оттенках.
    #else:
    #    cv2.imshow('Window', gray)

    cv2.imshow('Window', frame) # просто для демонстрации работы, чтобы пользователь видел что скрипт не завис
    prev_frame=gray
    key=cv2.waitKey(1)
    if key == ord('q'):
        break

print(f'Всего видео содержит {counter} изображений свитка.')
camera.release()
cv2.destroyAllWindows()