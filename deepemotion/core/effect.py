# -*- coding: utf-8 -*-
######## REFs face detection ########
# https://www.superdatascience.com/opencv-face-detection/
#####################################

from keras.models import load_model
from keras import backend as K
import tensorflow as tf

import os
import numpy as np
import cv2

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.environ["CUDA_VISIBLE_DEVICES"] = "" # do not use the GPU

img_rows, img_cols = 48, 48

labels_txt = np.array(['Colère', 'Peur', 'Joie', 'Tristesse', 'Surprise', 'Neutre'])

num_classes = labels_txt.size

graph = tf.get_default_graph()
model = load_model(r'/home/jeremie/jeremie/topten/static/model/trained_model')
IMP = np.load(r'/home/jeremie/jeremie/topten/static/model/IMP.npy')
print "model loaded"

face_cascade = cv2.CascadeClassifier()
face_cascade_name = "/home/jeremie/miniconda2/envs/keras/lib/python2.7/site-packages/cv2/data/haarcascade_frontalface_default.xml"
face_cascade.load(face_cascade_name)
print "face detector loaded"

def transform_image(im):
    im2 = im.astype(np.float32)*1
    im2 -= 127.817
    im2 /= 74.3659
    return im2

def cut_face(im, cascade_classifier):
    faces = cascade_classifier.detectMultiScale(im)
    print(len(faces), "face(s) detected")
    if len(faces) != 0:
        x, y, w, h = [ v for v in faces[0] ]
        return im[y:y+h, x:x+w]
    else:
        return im*0
    return im
 
def reconstruct_image(im):
    im2 = im.astype(np.float32)*1
    im2 *= 74.3659
    im2 += 127.817
    return np.squeeze(im2.astype(np.uint8))

def transform(fname):
    image_path = fname
    custom_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    custom_image = cut_face(custom_image, face_cascade)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    custom_input = clahe.apply(custom_image)
    
    sh = custom_input.shape
    custom_input = cv2.resize(custom_input, (img_rows, img_cols))
    custom_input = transform_image(custom_input)
    custom_input = np.expand_dims(custom_input, axis=0)
    custom_input = np.expand_dims(custom_input, axis=0)
    with graph.as_default():
        res1 = model.predict(custom_input, verbose=0)[0]
        res2 = model.predict(np.fliplr(custom_input), verbose=0)[0]
        res = (res1+res2)/2.
        k = np.argmax(res)
        
        input_img = model.layers[0].input
        for l in model.layers:
            if(l.name == 'last_conv'):
                layer_output = l.output
        get_acti = K.function([input_img, K.learning_phase()], [layer_output[:,:,:,:]])
        
        fig = plt.figure()
        img = np.zeros((sh[0], sh[1]))
        acti = np.squeeze(get_acti([custom_input,0])[0])
        for i in range(IMP[k].size):
            img += IMP[k][i]*cv2.resize(np.abs(acti[i]), (sh[1], sh[0]))
        plt.imshow(custom_image, cmap='gray')
        plt.imshow(img, alpha=0.4, cmap='bwr')
        plt.axis('off')
        fig.tight_layout()
        fig.savefig("static/temp2.jpeg")
    return res[0], labels_txt[k]

