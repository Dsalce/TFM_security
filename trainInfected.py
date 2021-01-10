# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 11:25:39 2020

@author: dsalc
"""

# -*- coding: utf-8 -*-

"Basado en https://machinelearningmastery.com/how-to-develop-a-face-recognition-system-using-facenet-in-keras-and-an-svm-classifier/"


from numpy import load
from numpy import expand_dims
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from matplotlib import pyplot
import os
import numpy
from os import listdir
from os.path import isdir
from PIL import Image
from numpy import savez_compressed
from numpy import asarray
from mtcnn.mtcnn import MTCNN
import tensorflow as tf
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import joblib

class TrainInfected(object):
   def __init__(self):
       pass
   
   def extract_face(self,filename,size=(160, 160)):
       
        #Carga imagen
        image = Image.open(filename)
        #convierte  a RGB
        image = image.convert('RGB')
        # convertir a array
        pixels = asarray(image)
        # crea el detector de caras
        detect = MTCNN()
        # Deteccion de caras
        boxes = detect.detect_faces(pixels)
        # Extraccion de la caja
        x1, y1, w, h = boxes[0]['box']
        
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + w, y1 + h
        # extracion de la cara
        face = pixels[y1:y2, x1:x2]
        # redimension de los pixeles de los array
        imagen = Image.fromarray(face)
        imagen = image.resize(size)
        face_array = asarray(imagen)
        return face_array
  
  
   def load_faces(self,direc):
      imagesFace = list()
      for file in listdir(direc):
        try:  
         path =os.path.join(direc,file)
         print(path)
         face = self.extract_face(path)
         imagesFace.append(face)
        except IndexError:
             pass
      return imagesFace
     
    # Carga dataset de caras
   def saveDataset(self):
        print("MTCNN")
        trainX, trainy = list(), list()
        direc='dataset/train/'
        # Carpetas de dataset
        for subdir in listdir(direc):
                path = direc + subdir + '/'
                if not isdir(path):
                 continue
                faces = self.load_faces(path)
                # crear etiquetas
                labels = [subdir for _ in range(len(faces))]
                print('Etiqueta entrenamiento: %s' % ( subdir))
                trainX.extend(faces)
                trainy.extend(labels)
        savez_compressed('trainInfectFace.npz', trainX, trainy)
            
    
  
   def get_embedding(self,model, facePixels):
        # reescalado de pixeles de imagenes
        facePixels = facePixels.astype('float32')
        mean, std = facePixels.mean(), facePixels.std()
        facePixels = (facePixels - mean) / std
        samples = expand_dims(facePixels, axis=0)
        # Obtencion de vector 
        emb = model.predict(samples)
        return emb[0]

   def embeddingDataset(self):
        print("FACENET")
        # Carga imagenes de caras
        data = load('trainInfectFace.npz')
        trainX, trainy = data['arr_0'], data['arr_1']
        # carga facenet 
        model = tf.keras.models.load_model('facenet_keras.h5')
        embsVector = list()
        for facePixels in trainX:
            embedding = self.get_embedding(model, facePixels)
            embsVector.append(embedding)
        embsVector = asarray(embsVector)

        savez_compressed('trainInfectEmbed.npz', embsVector, trainy)

   def identifyPerson(self):
        # Carga de vectores
        data = numpy.load('trainInfectEmbed.npz')
        trainX, trainy = data['arr_0'], data['arr_1']
        inEncoder = Normalizer(norm='l2')
        trainX = inEncoder.transform(trainX)
        
        # Transforma la etiqueta en 0 o 1
        outEncoder = LabelEncoder()
        outEncoder.fit(trainy)
        trainy = outEncoder.transform(trainy)
        # Entrenamiento de MVS
        #model = SVC(kernel='linear',class_weight={0: 1, 1: 2}, probability=True,verbose=True, )
        model = SVC(kernel='rbf' ,class_weight={0: 1, 1: 2}, probability=True,verbose=True,)
        model.fit(trainX, trainy)
        # Guardar modelo
        joblib.dump(model, 'modelInfect.sav')
         
   


if __name__ == '__main__':
    
    person = TrainInfected()
    # load train dataset
    #person.saveDataset()
    #person.embeddingDataset()
    person.identifyPerson()
