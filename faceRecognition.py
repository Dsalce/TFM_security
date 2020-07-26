# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 11:46:00 2020

@author: dsalc
"""

import tensorflow as tf
AUTOTUNE = tf.data.experimental.AUTOTUNE
import IPython.display as display
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
from easyfacenet.simple import facenet

class flower(object):
    def __init__(self):
       pass
   
    def show_batch(self,image_batch, label_batch):
       plt.figure(figsize=(10,10))
       for n in range(25):
        ax = plt.subplot(5,5,n+1)
        plt.imshow(image_batch[n])
        plt.title(CLASS_NAMES[label_batch[n]==1][0].title())
        plt.axis('off')

       
     #Write a short pure-tensorflow function that converts a file path to an (img, label) pair:
    def get_label(self,file_path):
      # convert the path to a list of path components
      parts = tf.strings.split(file_path, os.path.sep)
      # The second to last is the class-directory
      return parts[-2] == CLASS_NAMES
  
    def decode_img(self,img):
     # convert the compressed string to a 3D uint8 tensor
     img = tf.image.decode_jpeg(img, channels=3)
     # Use `convert_image_dtype` to convert to floats in the [0,1] range.
     img = tf.image.convert_image_dtype(img, tf.float32)
     # resize the image to the desired size.
     return tf.image.resize(img, [self.IMG_HEIGHT, self.IMG_WIDTH])
 
    
    def process_path(self,file_path):
      label = self.get_label(file_path)
      # load the raw data from the file as a string
      img = tf.io.read_file(file_path)
      img = self.decode_img(img)
      return img, label
  
    def prepare_for_training(self,ds, cache=True, shuffle_buffer_size=1000):
      # This is a small dataset, only load it once, and keep it in memory.
      # use `.cache(filename)` to cache preprocessing work for datasets that don't
      # fit in memory.
      if cache:
        if isinstance(cache, str):
          ds = ds.cache(cache)
        else:
          ds = ds.cache()

      ds = ds.shuffle(buffer_size=shuffle_buffer_size)
    
      # Repeat forever
      ds = ds.repeat()
    
      ds = ds.batch(BATCH_SIZE)
    
      # `prefetch` lets the dataset fetch batches in the background while the model
      # is training.
      ds = ds.prefetch(buffer_size=AUTOTUNE)
    
      return ds

    def test(self):
        """ data_dir = tf.keras.utils.get_file(origin='https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
                                         fname='flower_photos', untar=True)
        data_dir = pathlib.Path(data_dir)
        image_count = len(list(data_dir.glob('*/*.jpg')))
        print(image_count)
        CLASS_NAMES = np.array([item.name for item in data_dir.glob('*') if item.name != "LICENSE.txt"])
        roses = list(data_dir.glob('roses/*'))"""

        

        #for image_path in roses[:3]:
         #          display.display(Image.open(str(image_path)))
                   
        # Set `num_parallel_calls` so multiple images are loaded/processed in parallel.
        
        list_ds = tf.data.Dataset.list_files(str("D:\Informatica\Seguridad informatica_UNIR\TFM\comor_codigo\image"+'*/*'))
        for f in list_ds.take(5):
           print(f.numpy())

        labeled_ds = list_ds.map(self.process_path, num_parallel_calls=AUTOTUNE)
        for image, label in labeled_ds.take(1):
              print("Image shape: ", image.numpy().shape)
              print("Label: ", label.numpy())
            
       
        
        
        train_ds = self.prepare_for_training(labeled_ds)
            
        image_batch, label_batch = next(iter(train_ds))
            
                       
                  
        show_batch(image_batch.numpy(), label_batch.numpy())








if __name__ == '__main__':
    
    flo = flower()
    flo.test()
