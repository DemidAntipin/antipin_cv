import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.ndimage.morphology import binary_dilation, binary_erosion, binary_closing, binary_opening

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

image=np.load("stars.npy").astype("u8")
struct_cross=np.array([[1,0,0,0,1],
                [0,1,0,1,0],
                [0,0,1,0,0],
                [0,1,0,1,0],
                [1,0,0,0,1]])
stars_cross=binary_erosion(image,struct_cross).astype("u8")
struct_plus=np.array([[0,0,1,0,0],
                [0,0,1,0,0],
                [1,1,1,1,1],
                [0,0,1,0,0],
                [0,0,1,0,0]])
stars_plus=binary_erosion(image,struct_plus).astype("u8")
image=stars_cross|stars_plus
print(np.unique(two_pass(image)).max())
