import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
from base64 import b64encode
backend=default_backend()

key_input=input("key: ")
hash_func=hashlib.sha256()
hash_func.update(bytes(key_input,'utf-8'))
key=hash_func.digest()
iv=os.urandom(16)
cipher=Cipher(algorithms.AES(key),modes.CTR(iv),backend=backend)
encryptor =cipher.encryptor()
plaintext=input("plaintext: ")
ct = encryptor.update(bytes(plaintext,'utf-8'))+encryptor.finalize()
print("cipher text:")
print(b64encode(ct).decode('utf-8'),end="")
print(b64encode(iv).decode('utf-8'),end="")