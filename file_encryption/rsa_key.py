
import os.path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

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
        #################
        ## PRIVATE KEY ##
        #################
        # Generate new RSA private key with given backend, e, and key size.
        key_private = rsa.generate_private_key( self.paramRsa[0], self.paramRsa[1],  default_backend() )
        
        # Serialize private key without encryption.
        pem_private = key_private.private_bytes(  serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption() )
        
        ################
        ## PUBLIC KEY ##
        ################
        # Generate new RSA public key using private key.
        key_public = key_private.public_key()
        
        # Serialize public key
        pem_public = key_public.public_bytes(  serialization.Encoding.PEM,  serialization.PublicFormat.SubjectPublicKeyInfo )
        
        
        ################
        ## POST  KEYS ##
        ################
        post_data = {}
        # Load data into collection
        post_data["private"] = b64encode(pem_private).decode("utf-8")
        post_data["public"] = b64encode(pem_public).decode("utf-8")
    
        
        
        print(post_data)
        
        # Write serialized key into file
        with open(self.paramRsa[2], 'wb') as file:
            file.write(pem_public)
            file.close()
            
        with open(self.paramRsa[3], 'wb') as file:
            file.write(pem_private)
            file.close()
            
        

if __name__ == "__main__": 
   key=RSAkeygeneration()
   key.genPrivPublic()