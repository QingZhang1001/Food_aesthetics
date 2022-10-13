
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import glob
import cv2
from skimage import feature


images=glob.glob('/home/IW_student/work/Allrecipe/allrecipes/*.jpg')

i=0
eps=1e-7
for img in images:
    print(img)
    i=i+1
    tail=img.split('/')[-1]
    print(tail)
    print(i)
    img_array=cv2.imread(img)
    img_array=cv2.resize(img_array,(224,224))
    img_gray=cv2.cvtColor(img_array,cv2.COLOR_BGR2GRAY)
    lbp=feature.local_binary_pattern(img_gray,24,8,method='uniform')
    (hist,_)=np.histogram(lbp.ravel(),bins=np.arange(0,24+3),
                         range=(0,24+2))
    hist=hist.astype('float')
    hist/=(hist.sum()+eps)
    hist=hist.reshape(1,-1)
    f=open('/home/IW_student/work/LBP_hist_extractors/allrecipes_lbp_full.csv','a')
    f.write(tail+',')
    np.savetxt(f,hist,delimiter=',')
    f.close()

