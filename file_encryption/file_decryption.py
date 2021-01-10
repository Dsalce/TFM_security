

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES,PKCS1_OAEP


CONST_LEN_KEY = 32
CONST_LEN_IV = 16
CONST_LEN_BLOCK = 128
CONST_KEY_PUBLIC_PATH = "rsa_key_public.pem"
CONST_KEY_PRIVATE_PATH = "rsa_key_private.pem"


        
def MyRSADecrypt(RSACipher, ciphertext, IV, tag, ext, RSA_Privatekey_filepath):
    # Obtener la clave privada
    key_priv = RSA.import_key(open(RSA_Privatekey_filepath).read())
        
    # Desencriptar la clave de sesion con la clave privada
    cipher_rsa = PKCS1_OAEP.new(key_priv)
    session_key = cipher_rsa.decrypt(RSACipher)
    # Desencriptado del fichero con la clave de sesion
    cipher_aes = AES.new(session_key, AES.MODE_EAX, IV)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    
    return data
    
    
    