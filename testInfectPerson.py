# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 10:22:22 2020

@author: dsalc
"""

# -*- coding: utf-8 -*-

"Basado en https://machinelearningmastery.com/how-to-develop-a-face-recognition-system-using-facenet-in-keras-and-an-svm-classifier/"


from numpy import load
from numpy import expand_dims
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer

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


class testInfectPerson(object):
   def __init__(self):
       pass
   
   def extract_face(self,filename,required_size=(160, 160)):
       
    	#load image from file
    	print(filename)
    	image = Image.open(filename)
    	#convert to RGB, if needed
    	image = image.convert('RGB')
    	# convert to array
    	pixels = asarray(image)
    	# create the detector, using default weights
    	detector = MTCNN()
    	# detect faces in the image
    	results = detector.detect_faces(pixels)
    	# extract the bounding box from the first face
    	x1, y1, width, height = results[0]['box']
    	# bug fix
    	x1, y1 = abs(x1), abs(y1)
    	x2, y2 = x1 + width, y1 + height
    	# extract the face
    	face = pixels[y1:y2, x1:x2]
    	# resize pixels to the model size
    	image = Image.fromarray(face)
    	image = image.resize(required_size)
    	face_array = asarray(image)
    	return face_array
  
   # load images and extract faces for all images in a directory
   def load_faces(self,directory):
    	faces = list()
    	# enumerate files
    	for filename in listdir(directory):
    		# path
    		path =os.path.join(directory,filename)
    		# get face
    		face = self.extract_face(path)
    		# store
    		faces.append(face)
    	return faces
     
    # load a dataset that contains one subdir for each class that in turn contains images
   def load_dataset(self,directory):
    	X, y = list(), list()
    	# enumerate folders, on per class
    	for subdir in listdir(directory):
    		# path
    		path = directory + subdir + '/'
    		# skip any files that might be in the dir
    		if not isdir(path):
    			continue
    		# load all faces in the subdirectory
    		faces = self.load_faces(path)
    		# create labels
    		labels = [subdir for _ in range(len(faces))]
    		# summarize progress
    		print('>loaded %d examples for class: %s' % (len(faces), subdir))
    		# store
    		X.extend(faces)
    		y.extend(labels)
    	return asarray(X), asarray(y)
   def saveDataset(self):
       
        # load test dataset
        testX, testy = self.load_dataset('dataset/val/')
        # save arrays to one file in compressed format
        savez_compressed('testInfect.npz', testX, testy)
    
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
        data = load('testInfect.npz')
        print(data)
        testX, testy = data['arr_0'], data['arr_1']
        print('Loaded: ', testX.shape, testy.shape)
        # load the facenet model
        model = tf.keras.models.load_model('facenet_keras.h5')
        print('Loaded Model')
        # convert each face in the train set to an embedding
    
        newTestX = list()
        for face_pixels in testX:
        	embedding = self.get_embedding(model, face_pixels)
        	newTestX.append(embedding)
        newTestX = asarray(newTestX)
        print(newTestX.shape)
        # save arrays to one file in compressed format
        savez_compressed('test_Infectemp.npz',  newTestX, testy)
   


   
   def identifyPerson(self):
        infected=False
       
        # load faces
        data = numpy.load('testInfect.npz')
        testX_faces = data['arr_0']
        # load face embeddings
        data = numpy.load('test_Infectemp.npz')
        testX, testy = data['arr_0'], data['arr_1']
        model = joblib.load('modelInfect.sav') 
        
        # normalize input vectors
        in_encoder = Normalizer(norm='l2')
        
        testX = in_encoder.transform(testX)
        
        out_encoder = LabelEncoder()
        
        out_encoder.fit(testy)
        
        testy = out_encoder.transform(testy)
        
        
        # test model on a random example from the test dataset
        predict=[]
        trueFace=[]
        infect=0
        name_class=""
        for selection in range(testX.shape[0]):
            random_face_pixels = testX_faces[selection]
            random_face_emb = testX[selection]
            random_face_class = testy[selection]
            random_face_name = out_encoder.inverse_transform([random_face_class])
            # prediction for the face
            samples = expand_dims(random_face_emb, axis=0)
            yhat_class = model.predict(samples)
            yhat_prob = model.predict_proba(samples)
            # get name
            class_index = yhat_class[0]
            class_probability = yhat_prob[0,class_index] * 100
            predict_names = out_encoder.inverse_transform(yhat_class)
            predict.append(predict_names)
            name_class=predict_names
            trueFace.append(random_face_name)
            print('Predicted: %s (%.3f)' % (predict_names[0], class_probability))
            print('Expected: %s' % random_face_name[0])
            
            pyplot.imshow(random_face_pixels)
            title = '%s (%.3f)' % (predict_names[0], class_probability)
            
            if(predict_names[0]=="infected"):
             infect=infect+1
            pyplot.title(title)
            pyplot.show()
            
        con=confusion_matrix(trueFace, predict)
        print(con)
        #self.confusionMatrix(con,testy,predict)
        titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
        for title, normalize in titles_options:
                disp = plot_confusion_matrix(model, testX, testy, display_labels=name_class, cmap=pyplot.cm.Blues,normalize=normalize)
                disp.ax_.set_title(title)
                
                print(title)
                print(disp.confusion_matrix)
        if (infect==10):
           infected=True        
   
        return infected


if __name__ == '__main__':
    
    person = testInfectPerson()
    # load train dataset
    #person.saveDataset()
    #person.embeddingDataset()
    person.identifyPerson()
