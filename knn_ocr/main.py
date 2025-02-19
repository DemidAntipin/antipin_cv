import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import cv2
from sklearn.neighbors import KNeighborsClassifier

p=Path('task/')

def load_data(path):
  images = []
  labels = []
  for label_path in path.joinpath('train').iterdir():
    label = label_path.name[-1]
    for f in sorted(label_path.glob('*.png')):
      img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
      _, binary_img = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY)
      # обрезаем изображение, чтобы объект занимал все пространство
      mask = np.zeros_like(binary_img)
      mask[binary_img > 0] = 1
      kernel = np.array([[0],[1],[1]], np.uint8)
      # нарашиваем маску, чтобы соединить контуры . и | в букве i
      dilated_mask = cv2.dilate(mask, kernel, iterations=15)
      contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      x, y, w, h = cv2.boundingRect(contours[0])
      binary_img = binary_img[y:y+h, x:x+w]
      binary_img = cv2.resize(binary_img, (128, 128))
      # искусственно увеличиваем датасет, копируя картинки (так лучше работает)
      images.append(binary_img.flatten())
      labels.append(ord(label))
      images.append(binary_img.flatten())
      labels.append(ord(label))
      images.append(binary_img.flatten())
      labels.append(ord(label))
  return np.float32(images), np.array(labels, dtype=np.int32)

data, labels = load_data(p)

knn = cv2.ml.KNearest_create()
knn.train(data, cv2.ml.ROW_SAMPLE, labels)

for j, file in enumerate(sorted(p.glob('*.png'))):
  image = cv2.imread(file)
  print(f'Изображение №{j}: ', end='')

  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  _, binary = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY)
  # Маска на 17 пикселей больше, чтобы при нарашивании не обрезались 17 верхних пикселей
  # 17 это max расстояние (среди картинок) между контурами элементов в букве i
  mask = np.zeros((binary.shape[0] + 17, binary.shape[1]), dtype=np.uint8)
  mask[17:, :] = binary > 0

  kernel = np.array([[0],[1],[1]], np.uint8)
  # соединяем контура в букве i
  dilated_mask = cv2.dilate(mask, kernel, iterations=17)
  # возвращаем буквам прежную высоту
  dilated_mask = cv2.erode(dilated_mask, kernel, iterations=17)
  contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  x_axes=[]
  contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
  for i, contour in enumerate(contours):
      x, y, w, h = cv2.boundingRect(contour)
      if x_axes:
        # примерное min расстояние по оси X в пикселях между словами
        if x-x_axes[-1]>30:
          print(' ', end='') #пробел между словами
      x_axes.append(x+w)

      symbol_image = binary[y:y+h, x:x+w]
      symbol_image = cv2.resize(symbol_image, (128, 128))
      symbol_image=symbol_image.flatten().reshape(1, -1)
      _, pred, _, _=knn.findNearest(np.float32(symbol_image), 3)
      print(chr(int(pred[0][0])), end='')
  print()