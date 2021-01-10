# -*- coding: utf-8 -*-




import os


from threading import Thread

import cv2
import time

class ObtainPicture(object):
    #Constructor
    def __init__(self):
       self.cam = cv2.VideoCapture(0)
       # Start the thread to read frames from the video stream
       self.thread = Thread(target=self.cameraExecute, args=())
       self.thread.daemon = True
       self.thread.start()
    
    def cameraExecute(self):
      while True:
        # Display frames in main program
        ret, frame = self.cam.read()
        if not ret:
                print("failed to grab frame")
                break
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.cam.release()
            cv2.destroyAllWindows()
            #exit(1)
    
    #Load .csv file
    def obtainPicture(self):
        path=os.path.abspath(os.getcwd())
      
        
        img_counter=0
        for i in range(5):
            ret, frame = self.cam.read()
            if not ret:
                print("failed to grab frame")
                break
          
            os.chdir(path)
            os.chdir("dataset/val/test/")
            img_name = "image_{}.jpg".format(img_counter)#os.path.join("\test2\train\infected","image_{}.jpg".format(img_counter))
            cv2.imwrite(img_name, frame)
            time.sleep(1)
            print("{} written!".format(img_name))
            """os.chdir(path)
            os.chdir("dataset/val/notinfected/")
            img_name = "image_{}.jpg".format(img_counter)#os.path.join("\test2\train\infected","image_{}.jpg".format(img_counter))
            cv2.imwrite(img_name, frame)
            time.sleep(1)
            print("{} written!".format(img_name))"""
            img_counter += 1
        
        
      
if __name__ == '__main__':
    
    p = ObtainPicture()
    p.obtainPicture()
    
    
    
    
    
    
      