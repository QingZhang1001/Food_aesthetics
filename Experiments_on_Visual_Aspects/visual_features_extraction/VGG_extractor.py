#ctrattner Oct 16 2018
# VGG16 feature extraction
#import matplotlib.pyplot as plt
import numpy as np
np.random.seed(2018)
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input #, decode_predictions
from keras.preprocessing import image
from keras.models import Model
import glob
import os

# load pre-trained model
model = VGG16(weights='imagenet', include_top=True)
# display model layers
model.summary()

# load pre-trained model
base_model = VGG16(weights='imagenet')
# pre-process the image
images = glob.glob("/Users/ctrattner/Desktop/Research/Movie-Data/images/*.jpg")

i = 0
for img_ in images:
    print(img_)
    i = i + 1
    head, tail = os.path.split(img_)
    print(tail)
    print(i)
    img = image.load_img(img_, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    # define model from base model for feature extraction from fc1 layer
    model = Model(input=base_model.input, output=base_model.get_layer('fc1').output)
    # obtain the output of fc1 layer
    fc1_features = model.predict(img)
    print("Feature vector dimensions: ",fc1_features)
    f = open('/Users/ctrattner/Desktop/test.out', "a")
    f.write(tail+",")
    np.savetxt(f, fc1_features, delimiter=',' ,fmt='%.16f')
    f.close()