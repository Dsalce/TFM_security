
import os


from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES,PKCS1_OAEP
from Cryptodome.Util.Padding import pad

CONST_LEN_KEY = 32
CONST_LEN_BLOCK_BYTES= 16
CONST_LEN_BLOCK = 128
CONST_KEY_PUBLIC_PATH = "rsa_key_public.pem"
CONST_KEY_PRIVATE_PATH = "rsa_key_private.pem"

class FileEncript(object):

# Global Constants
    
    def __init__(self):
        pass
    
    
    
    def MyRSAEncrypt(self,filepath, RSA_Publickey_filepath):
        
        
        name, ext = os.path.splitext(filepath)
        recipient_key = RSA.importKey(open(RSA_Publickey_filepath).read())
        session_key = get_random_bytes(CONST_LEN_KEY)
        # Encripta la clave de sesion con la clave publica
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        
        # Se encriptan los datos con la clave de sesión
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        
        with open(filepath, "rb") as file:
            M = file.read()
            file.close()
        ciphertext, tag = cipher_aes.encrypt_and_digest(pad(M, CONST_LEN_BLOCK))
        
        return enc_session_key,ciphertext, cipher_aes.nonce, tag , ext