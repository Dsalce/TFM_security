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
        trainX, trainy = self.load_dataset('dataset/train/')
        print(trainX.shape, trainy.shape)
        # load test dataset
        
        # save arrays to one file in compressed format
        savez_compressed('trainInfectFace.npz', trainX, trainy)
    
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
        data = load('trainInfectFace.npz')
        print(data)
        trainX, trainy = data['arr_0'], data['arr_1']
        print('Loaded: ', trainX.shape, trainy.shape)
        # load the facenet model
        model = tf.keras.models.load_model('facenet_keras.h5')
        print('Loaded Model')
        # convert each face in the train set to an embedding
        newTrainX = list()
        for face_pixels in trainX:
        	embedding = self.get_embedding(model, face_pixels)
        	newTrainX.append(embedding)
        newTrainX = asarray(newTrainX)
        print(newTrainX.shape)
        # convert each face in the test set to an embedding
        
        # save arrays to one file in compressed format
        savez_compressed('trainInfectEmbed.npz', newTrainX, trainy)

   def identifyPerson(self):
        infected=False
       
       
        # load face embeddings
        data = numpy.load('trainInfectEmbed.npz')
        trainX, trainy = data['arr_0'], data['arr_1']
        # normalize input vectors
        in_encoder = Normalizer(norm='l2')
        trainX = in_encoder.transform(trainX)
        
        # label encode targets
        out_encoder = LabelEncoder()
        out_encoder.fit(trainy)
        trainy = out_encoder.transform(trainy)
    
        # fit model
        model = SVC(kernel='linear', probability=True,verbose=True,)
        #model = SVC(kernel='rbf', probability=True,verbose=True)
        model.fit(trainX, trainy)
        joblib.dump(model, 'modelInfect.sav')
         
   
        return infected


if __name__ == '__main__':
    
    person = TrainInfected()
    # load train dataset
    person.saveDataset()
    person.embeddingDataset()
    person.identifyPerson()
