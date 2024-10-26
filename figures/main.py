import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_dilation, binary_erosion, binary_closing, binary_opening

def neighbours2(y,x):
  return ((y,x-1),(y-1,x))

def exist(B, nbs):
  left, top = nbs
  if left[1]>=0 and left[1]<B.shape[1]:
    if B[left]==0:
      left=None
  else:
    left=None
  if top[0]>=0 and top[0]<B.shape[0]:
    if B[top]==0:
      top=None
  else:
    top=None
  return left, top

def find(label, linked):
  j=label
  while linked[j]!=0:
    j=linked[j]
  return j

def union(label1, label2, linked):
  j = find(label1,linked)
  k = find(label2, linked)
  if j!=k:
    linked[k]=j

def two_pass(B):
  LB=np.zeros_like(B)
  linked = np.zeros(B.size//2+1,dtype="uint")
  label=1
  for y in range(LB.shape[0]):
    for x in range(LB.shape[1]):
      if B[y,x]!=0:
        nbs=neighbours2(y,x)
        existed = exist(B, nbs)
        if existed[0] is None and existed[1] is None:
          m= label
          label+=1
        else:
          lbs = [LB[n] for n in existed if n is not None]
          m= min(lbs)
        LB[y,x]=m
        for n in existed:
          if n is not None:
            lb = LB[n]
            if lb !=m:
              union(m,lb,linked)
  for y in range(LB.shape[0]):
    for x in range(LB.shape[1]):
      if B[y,x] != 0:
        new_label = find(LB[y,x], linked)
        if new_label != LB[y,x]:
          LB[y,x]=new_label
  for fig, i in enumerate(np.unique(LB)):
      LB[LB==i]=fig
  return LB

def remove_rects(LB, t):
  struct=np.ones((3,3))
  rects=binary_opening(LB,struct).astype("u8")
  print(f"Фигур типа {t}:",two_pass(rects).max())
  return LB-rects

def dilate_figures(image, struct):
  dilation = binary_erosion(image, struct).astype("u8")
  dilated_image=image|dilation
  return dilated_image

def closing_figures(image, struct):
  return binary_closing(image,struct).astype("u8")
  

image=np.load("ps.npy.txt").astype("u8")
print("Всего фигур:",two_pass(image).max())
plt.subplot(231)
plt.imshow(image)
plt.title("Исходное изображение")
# Прямоугольники
image=remove_rects(image, "прямоугольник")
figure=np.array([[0,0,0,0,0,0,0,0],
                 [0,1,1,1,1,1,1,0],
                 [0,1,1,1,1,1,1,0],
                 [0,1,1,1,1,1,1,0],
                 [0,1,1,1,1,1,1,0],
                 [0,0,0,0,0,0,0,0]])
plt.subplot(232)
plt.imshow(figure)
plt.title("Прямоугольник")
# Подкова вверх
struct=np.array([[0,0,0,0,0],
                 [0,0,0,0,0],
                 [1,1,0,0,1],
                 [1,1,0,0,1],
                 [1,1,1,1,1]])
dilated_image=dilate_figures(image,struct)
struct=np.array([[0,0,0],
                [1,1,0],
                [0,0,0]])
closed_figures=closing_figures(dilated_image, struct)
image=remove_rects(closed_figures, "подкова вверх")
figure=np.array([[0,0,0,0,0,0,0,0],
                 [0,1,1,0,0,1,1,0],
                 [0,1,1,0,0,1,1,0],
                 [0,1,1,1,1,1,1,0],
                 [0,1,1,1,1,1,1,0],
                 [0,0,0,0,0,0,0,0]])
plt.subplot(233)
plt.imshow(figure)
plt.title("Подкова вверх")
# Подкова вниз
struct=np.array([[1,1,1,1,1],
                 [1,0,0,1,1],
                 [1,0,0,1,1],
                 [0,0,0,0,0],
                 [0,0,0,0,0]])
dilated_image=dilate_figures(image,struct)
struct=np.array([[0,0,0],
                [1,1,0],
                [0,0,0]])
closed_figures=closing_figures(dilated_image, struct)
image=remove_rects(closed_figures, "подкова вниз")
figure=np.array([[0,0,0,0,0,0,0,0],
                 [0,1,1,1,1,1,1,0],
                 [0,1,1,1,1,1,1,0],
                 [0,1,1,0,0,1,1,0],
                 [0,1,1,0,0,1,1,0],
                 [0,0,0,0,0,0,0,0]])
plt.subplot(234)
plt.imshow(figure)
plt.title("Подкова вниз")
# Подкова вправо
struct=np.array([[1,1,1,1,0,0,0],
                 [1,1,0,0,0,0,0],
                 [1,1,0,0,0,0,0],
                 [1,1,0,0,0,0,0],
                 [1,1,0,0,0,0,0]])
dilated_image=dilate_figures(image,struct)
struct=np.array([[0,0,0],
                [1,1,0],
                [0,0,0]])
closed_figures=closing_figures(dilated_image, struct)
image=remove_rects(closed_figures, "подкова вправо")
figure=np.array([[0,0,0,0,0,0],
                 [0,1,1,1,1,0],
                 [0,1,1,1,1,0],
                 [0,1,1,0,0,0],
                 [0,1,1,0,0,0],
                 [0,1,1,1,1,0],
                 [0,1,1,1,1,0],
                 [0,0,0,0,0,0]])
plt.subplot(235)
plt.imshow(figure)
plt.title("Подкова вправо")
# Подкова влево
struct=np.array([[0,0,0,1,1,1,1],
                 [0,0,0,0,0,1,1],
                 [0,0,0,0,0,1,1],
                 [0,0,0,0,0,1,1],
                 [0,0,0,0,0,1,1]])
dilated_image=dilate_figures(image,struct)
struct=np.array([[0,0,0],
                [0,1,1],
                [0,0,0]])
closed_figures=closing_figures(dilated_image, struct)
image=remove_rects(closed_figures, "подкова влево")
figure=np.array([[0,0,0,0,0,0],
                 [0,1,1,1,1,0],
                 [0,1,1,1,1,0],
                 [0,0,0,1,1,0],
                 [0,0,0,1,1,0],
                 [0,1,1,1,1,0],
                 [0,1,1,1,1,0],
                 [0,0,0,0,0,0]])
plt.subplot(236)
plt.imshow(figure)
plt.title("Подкова влево")
plt.show()


