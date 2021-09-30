import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
from base64 import b64decode,b64encode

def transfrom(data):
    return b64decode(bytes(data,"utf-8"))
backend=default_backend()
key_input=input("key: ")
ct_input=input("cipher text: ")
# iv=input("IV: ")
hash_func=hashlib.sha256()
hash_func.update(bytes(key_input,'utf-8'))
key=hash_func.digest()

cipher_text=ct_input[0:len(ct_input)-24]
iv=ct_input[len(ct_input)-24:len(ct_input)]

cipher=Cipher(algorithms.AES(key),modes.CTR(transfrom(iv) ),backend=backend)
decrytor=cipher.decryptor()
pt=decrytor.update(transfrom(cipher_text))+decrytor.finalize()
print("plain text:\n",pt.decode('utf-8'))