
# coding: utf-8

# In[1]:


import cv2
import os
import glob
import pandas as pd
import numpy as np


# In[ ]:


path='/home/IW_student/work/Allrecipe/allrecipes'
imgs=glob.glob('/home/IW_student/work/Allrecipe/allrecipes/*.jpg')


# In[ ]:


i=0
for img in imgs:
    print(img)
    i=i+1
    tail=img.split('/')[-1]
    print(tail)
    print(i)
    image=cv2.imread(img)
    image=cv2.resize(image,(224,224))
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    color_hist=cv2.calcHist([image],[0,1,2],None,[8,8,8],[0, 256, 0, 256, 0, 256])
    color_hist=cv2.normalize(color_hist,color_hist).flatten()
    color_hist=color_hist.reshape(1,-1)
    print('hist dimensions:',color_hist.shape)
    # write the histograms into csv
    f=open('/home/IW_student/work/color_hist_extractors/allrecipes_3dch_full.csv', "a")
    f.write(tail+',')
    np.savetxt(f,color_hist,delimiter=',')
    f.close()

