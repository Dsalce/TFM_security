
import os.path

from Cryptodome.PublicKey import RSA
from base64 import b64encode

class RSAkeygeneration(object):
    # Global Constants
    
    def __init__(self):
        self.paramRsa=[65537,2048,"rsa_key_public.pem","rsa_key_private.pem"]
    
    def genPrivPublic(self):
        if not self.haskeys():
            self.keygen()
    
    def haskeys(self):
        # Check for rsa_key_public.pem and rsa_key_private.pem in program root dir
        if not os.path.isfile(self.paramRsa[2]):
            print("Missing keys.")
            print("[!] Keys will be generated [!]")
            return False
        else:
            print("Public and Private keys exist.")
            return True
    
    def keygen(self): 
        
        key = RSA.generate(self.paramRsa[1])
        private_key = key.exportKey()
        file_out = open(self.paramRsa[3], "wb")
        file_out.write(private_key)
        file_out.close()
        
        public_key = key.publickey().exportKey()
        file_out = open(self.paramRsa[2], "wb")
        file_out.write(public_key)
        file_out.close()
        
            
        

if __name__ == "__main__": 
   key=RSAkeygeneration()
   key.genPrivPublic()