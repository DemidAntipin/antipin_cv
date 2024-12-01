import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

directory = 'out'
images=[]

for i in range(100):
    filename = f'h_{i}.npy'
    file_path = os.path.join(directory, filename)
    img = np.load(file_path).astype(np.uint8)
    images.append(img)

trajectory={}

def min_dist(x, y, arrs):
    id_of_min=-1
    min_dist=1e1000
    for i, item in enumerate(trajectory.values()):
            if i not in arrs:
                continue
            x1=item[-1][0]
            y1=item[-1][1]
            dist=((x1-x)**2+(y1-y)**2)**0.5
            if dist<min_dist:
                min_dist=dist
                id_of_min=i
    return id_of_min


cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(cnts)):
    trajectory[i]=[]
    (x,y), _ = cv2.minEnclosingCircle(cnts[i])
    trajectory[i].append((x,y))

for img in images[1:]:
    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cnts:
        (x,y), _ = cv2.minEnclosingCircle(cnt)
        arrs=list(i for i in trajectory.keys())
        id_of_min=min_dist(x, y, arrs)
        min_len=min(len(arr) for arr in trajectory.values())
        while min_len!=len(trajectory[id_of_min]):
            arrs.remove(id_of_min)
            id_of_min=min_dist(x, y, arrs)
            
        trajectory[id_of_min].append((x,y))

plt.figure(figsize=(10,10))
for i in trajectory.keys():
    trag=np.array(trajectory[i])
    plt.plot(trag[:, 0], trag[:, 1])
plt.show()