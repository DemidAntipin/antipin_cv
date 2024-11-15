import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, euler_number
from collections import defaultdict
from scipy.ndimage import binary_closing

def recognize(region):
  if region.image.mean()==1:
    return "-"
  else:
    image=region.image.copy()
    struct=np.array([[0,0,0],
                     [0,1,1],
                     [0,0,0]])
    image=binary_closing(image,struct)
    enumber=euler_number(image, 2)
    if enumber == -1:
      have_vl=np.sum(np.mean(region.image[:,:region.image.shape[1]//2], 0) == 1) > 3
      if have_vl:
        return "B"
      else:
        return "8"
    elif enumber == 0:
      have_vl=np.sum(np.mean(region.image, 0) == 1) > 3
      if have_vl:
        area=region.area_filled/region.image.size
        if area>0.8:
          return "D"
        else:
          return "P"
      else:
        image = region.image.copy()
        image[-1, :]=1
        enumber= euler_number(image,2)
        if enumber==-1:
          return "A"
        else:
          return "0"
    else:
      have_vl=np.sum(np.mean(region.image, 0) == 1) > 3
      if have_vl:
        return "1"
      else:
        if region.eccentricity<0.5:
          return "*"
        else:
          image=region.image.copy()
          image[0, :]=1
          image[-1, :]=1
          image[:,0]=1
          image[:,-1]=2
          enumber=euler_number(image)
          if enumber==-1:
            return "/"
          elif enumber==-3:
            return "X"
          else:
            return "W"
  return "@"

image=plt.imread("symbols.png")[:,:,:3].astype("f4").mean(2)
image=image>0

template=plt.imread("alphabet_ext.png")[:,:,:3].astype("f4").mean(2)
template[template<1]=0
template=np.logical_not(template)

labeled=label(image)

regions=regionprops(labeled)

result=defaultdict(lambda: 0)
for region in regions:
  symbol=recognize(region)
  result[symbol]+=1

print(result)

