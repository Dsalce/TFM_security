# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 12:10:40 2020

@author: dsalc
"""


"Basado en https://machinelearningmastery.com/how-to-develop-a-face-recognition-system-using-facenet-in-keras-and-an-svm-classifier/"


from numpy import load
from numpy import expand_dims
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn import metrics
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
from sklearn.metrics import plot_confusion_matrix
import itertools


class TestInfect(object):
   def __init__(self):
       pass
    
   def extract_face(self,filename,size=(160, 160)):
       
        #Carga imagen
        image = Image.open(filename)
        image = image.convert('RGB')
        pixels = asarray(image)
        # crea el detector de caras
        detect = MTCNN()
        # Deteccion de caras
        boxes = detect.detect_faces(pixels)
        # Extracción de la caja
        x1, y1, w, h = boxes[0]['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + w, y1 + h
        # Extracción de la cara
        face = pixels[y1:y2, x1:x2]
        # Redimensión de los pixeles de los array
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
        trainX, trainy = list(), list()
        direc='dataset/test/'
        for subdir in listdir(direc):
                path = direc + subdir + '/'
                if not isdir(path):
                 continue
                faces = self.load_faces(path)
                lab = [subdir for _ in range(len(faces))]
                print('>Etiqueta test: %s' % (subdir))
                trainX.extend(faces)
                trainy.extend(lab)
        savez_compressed('testInfectTEST.npz', trainX, trainy)
    
    
   # get the face embedding for one face
   def get_embedding(self,model, face_pixels):
        # scale pixel values
        face_pixels = face_pixels.astype('float32')
    	# standardize pixel values across channels (global)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        # transform face into one sample
        samples = expand_dims(face_pixels, axis=0)
        # make prediction to get embedding
        yhat = model.predict(samples)
        return yhat[0]

   def embeddingDataset(self):
        # load the face dataset
        data = load('testInfectTEST.npz')
        print(data)
        testX, testy = data['arr_0'], data['arr_1']
   
        print('Loaded: ', testX.shape,testy.shape)
        # load the facenet model
        model = tf.keras.models.load_model('facenet_keras.h5', compile=False)
        print('Loaded Model')
        # convert each face in the train set to an embedding
    
        newTestX = list()
        for face_pixels in testX:
            embedding = self.get_embedding(model, face_pixels)
            newTestX.append(embedding)
        newTestX = asarray(newTestX)
        print(newTestX.shape)
        # save arrays to one file in compressed format
        savez_compressed('test_InfectempTEST.npz', newTestX, testy)
   
    

   
   def identifyPerson(self):
        infected=False
       
        #  Cargar caras
        data = numpy.load('testInfectTEST.npz')
        testXFaces = data['arr_0']
        # Cargar vectores
        data = numpy.load('test_InfectempTEST.npz')
        testX, testy = data['arr_0'], data['arr_1']
       
        model = joblib.load('modelInfect.sav') 
        # Nor malizar vctores a 0 e 1
        testXencoder = Normalizer(norm='l2')
       
        testX = testXencoder.transform(testX)
        
        testyEncoder = LabelEncoder()
        
        testyEncoder.fit(testy)
        
        testy = testyEncoder.transform(testy)
        
        
        # test model on a random example from the test dataset
        predictMatix=[]
        trueFace=[]
        infect=0
        scores=[]
      
        for selection in range(testX.shape[0]):
            pixelsFace= testXFaces[selection]
            faceEmb = testX[selection]
            faceType = testy[selection]
            faceLabel = testyEncoder.inverse_transform([faceType])
            # prediccion para la cara
            predict = expand_dims(faceEmb, axis=0)
            predictClass = model.predict(predict)
            predictProb = model.predict_proba(predict)
            # get name
            index = predictClass[0]
            prob = predictProb[0,index] * 100
            predictLabel = testyEncoder.inverse_transform(predictClass)
            scores.append(prob)
            predictMatix.append(predictLabel)
            
            trueFace.append(faceLabel)
            print('Predicted: %s (%.3f)' % (predictLabel[0], prob))
            print('Expected: %s' % faceLabel[0])
            
            pyplot.imshow(pixelsFace)
            title = '%s (%.3f)' % (predictLabel[0], prob)
            
            if(predictLabel[0]=="infected"):
             infect=infect+1
            pyplot.title(title)
            pyplot.show()
            
            
            
        #Matriz de confusión
        con=confusion_matrix(trueFace, predictMatix)
        print(con)
        titles_options = [("Confusion matrix", None)]
        for title, normalize in titles_options:
                disp = plot_confusion_matrix(model, testX, testy, display_labels=["infected","notinfected"], cmap=pyplot.cm.Blues,normalize=normalize)
                disp.ax_.set_title(title)
                
                print(title)
                print(disp.confusion_matrix)
                
               
                

                
               
        auc= metrics.roc_auc_score(testy, scores)
        
        print("El AUC es de:",auc)
        
        #Genera ROC
        fpr, tpr, thresholds = metrics.roc_curve(testy, scores)
        
        pyplot.figure()
        lw = 2
        pyplot.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve  (AUC = %0.2f)' % auc)
        pyplot.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        pyplot.xlim([-0.001, 1.0])
        pyplot.ylim([-0.001, 1.05])
        pyplot.xlabel('False Positive Rate')
        pyplot.ylabel('True Positive Rate')
        pyplot.title('ROC/AUC')
        pyplot.legend(loc="lower right")
        pyplot.show()

        if (infect==10):
           infected=True        
   
        return infected


if __name__ == '__main__':
    
    person = TestInfect()
    # load train dataset
   #person.saveDataset()
    #person.embeddingDataset()
    person.identifyPerson()
