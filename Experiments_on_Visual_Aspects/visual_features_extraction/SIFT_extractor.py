
# coding: utf-8

# In[7]:


import cv2 
import numpy as np
import os
import glob
import pandas as pd
from sklearn.cluster import KMeans,MiniBatchKMeans
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import time


# In[8]:


os.getcwd()


# In[9]:


xiachufang_imgs=set(glob.glob('/home/IW_student/work/full/*.jpg'))
#allrecipes_imgs_001=set(glob.glob('/home/IW_student/work/Allrecipe/allrecipes_images_001/*.jpg'))
#allrecipes_imgs_002=set(glob.glob('/home/IW_student/work/Allrecipe/allrecipes_images_002/*.jpg'))
#allrecipes_imgs=allrecipes_imgs_001|allrecipes_imgs_002
allrecipes_imgs=set(glob.glob('/home/IW_student/work/Allrecipe/allrecipes/*.jpg'))
kochbar_imgs_001=set(glob.glob('/home/IW_student/work/Kochbar/kochbar_001/*.jpg'))
kochbar_imgs_002=set(glob.glob('/home/IW_student/work/Kochbar/kochbar_002/*.jpg'))
kochbar_imgs_003=set(glob.glob('/home/IW_student/work/Kochbar/kochbar_003/*.jpg'))
kochbar_imgs=kochbar_imgs_001|kochbar_imgs_002|kochbar_imgs_003


# In[10]:


labeled_img_paths = [[path, 0] for path in xiachufang_imgs] + [[path, 1] for path in allrecipes_imgs]+[[path, 2] for path in kochbar_imgs]


# In[11]:


print(len(labeled_img_paths))


# In[12]:


# extract the features
def gen_sift_features(labeled_img_paths):
    img_descs=[]
    error_list=[]
    id_list=[]
    i=0
    for img,label in labeled_img_paths:
        tail=img.split('/')[-1]
        id_list.append(tail)
        #print(tail)
        i=i+1
        #print(i)
        image=cv2.imread(img)
        image=cv2.resize(image,(224,224))
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        sift=cv2.xfeatures2d.SIFT_create()
        kps,descs=sift.detectAndCompute(gray, None)
        try:
            #print(descs.shape)
            if(descs.shape[1]==128):
                img_descs.append(descs)
        except AttributeError:
            print('shape not found for:' + img,i)
            error_list.append(i)
    y=np.array(labeled_img_paths)[:,1]
    return img_descs,y,error_list,id_list


# In[13]:


img_descs,y,error_list,id_list=gen_sift_features(labeled_img_paths)


# In[14]:


len(img_descs) # SIFT descriptors for each image


# In[ ]:


error_list=[i-1 for i in error_list]
y=[y[i] for i in range(len(y)) if(i not in error_list)]
id_list=[id_list[i] for i in range(len(id_list)) if(i not in error_list)]
rc=pd.DataFrame({'recipe_id':id_list,
                'class':y})
rc.to_csv('727_recipe_id_class.csv')


# In[ ]:


all_descs=[desc for desc_list in img_descs for desc in desc_list]
all_descs=np.array(all_descs)


# In[ ]:


all_descs.shape


# In[ ]:


if all_descs.shape[1] != 128:
    raise ValueError('Expected SIFT descriptors to have 128 features, got', all_descs.shape[1])
print ('%i descriptors before clustering' % all_descs.shape[0]) # 3个数据集中的133900幅图，共提取出33450576个SIFT descriptors


# In[ ]:


n_clusters=500
cluster_model=MiniBatchKMeans(n_clusters=500,random_state=0,batch_size=100)


# In[ ]:


print ('Using clustering model %s...' % repr(cluster_model))
print ('Clustering on training set to get codebook of %i words' % n_clusters)


# In[ ]:


time_0=time.time()


# In[ ]:


cluster_model.fit(all_descs)
print ('done clustering. Using clustering model to generate BoW histograms for each image.')
print(time.time()-time_0)


# In[ ]:


img_clustered_words = [cluster_model.predict(raw_words) for raw_words in img_descs]


# In[ ]:


img_bow_hist=np.array([np.bincount(clustered_words, minlength=n_clusters) for clustered_words in img_clustered_words])
np.savetxt('img_bow_hist_full.csv',img_bow_hist,delimiter=',')


# In[ ]:


data=pd.read_csv('img_bow_hist_full.csv',header=None)
data.shape


# In[46]:


data.rename(columns=lambda x:'BOW'+str(x+1),inplace=True)


# In[ ]:


data.head()


# In[48]:


rc=pd.read_csv('727_recipe_id_class.csv',index_col=0)
rc.shape


# In[49]:


recipe_SIFT=pd.concat([rc.iloc[:,0],data,rc.iloc[:,1]],axis=1)
recipe_SIFT.shape


# In[51]:


recipe_id=[i.split('.')[0] for i in recipe_SIFT['recipe_id']]
recipe_SIFT['recipe_id']=pd.Series(recipe_id)


# In[52]:


recipe_SIFT.head()


# In[53]:


recipe_SIFT.to_csv('recipe_SIFT.csv')


# In[54]:


xiachufang_SIFT=recipe_SIFT[recipe_SIFT['class']==0]


# In[55]:


allrecipes_SIFT=recipe_SIFT[recipe_SIFT['class']==1]


# In[56]:


kochbar_SIFT=recipe_SIFT[recipe_SIFT['class']==2]


# In[57]:


xiachufang_SIFT.to_csv('/home/IW_student/work/Datasets/xiachufang_origin_datasets/xiachufang_SIFT_727.csv')
allrecipes_SIFT.to_csv('/home/IW_student/work/Datasets/allrecipes_origin_datasets/allrecipes_SIFT_727.csv')
kochbar_SIFT.to_csv('/home/IW_student/work/Datasets/kochbar_origin_datasets/kochbar_SIFT_727.csv')

