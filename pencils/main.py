import cv2
import os

directory = 'images'
images=[]
pencils_set={}

for i in range(12):
    filename = f'img ({i+1}).jpg'
    file_path = os.path.join(directory, filename)
    img = cv2.imread(file_path)
    images.append(img)

for i,img in enumerate(images):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (29,29), 0)
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
    thresh=cv2.bitwise_not(thresh)
    thresh = cv2.dilate(thresh, None, iterations=5)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cur_image_pencils={}
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area < 100000:
            continue
        (cx,cy), (w,h), _ = cv2.minAreaRect(cnt)
        if (w/h>12 or h/w>12):
            color=hsv[int(cy), int(cx)][0]
            color_exist=False
            for noise in range(-5, 6, 1):
                new_color=str(int(color)+noise)
                if new_color in cur_image_pencils.keys():
                    color_exist=True
                    cur_image_pencils[new_color]+=1
                    break
            if not color_exist:
                cur_image_pencils[f"{int(color)}"]=1
    for key in cur_image_pencils.keys():
        color_found=False
        for noise in range(-5, 6, 1):
            new_key=str(int(key)+noise)
            if new_key in pencils_set.keys():
                pencils_set[new_key]=max(pencils_set[new_key], cur_image_pencils[key])
                color_found=True
                break
        if not color_found:
            pencils_set[key]=cur_image_pencils[key]
    print(f"На изображении {i} - {sum(cur_image_pencils.values())} карандаш(-ей/-а)")
print(f"Всего в наборе {sum(pencils_set.values())} карандаш(-ей/-а).")