from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib

def pad(data):
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    return data[:-data[-1]]

def get_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(data, password):
    key = get_key(password)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data))
    return iv + encrypted

def decrypt_file(data, password):
    key = get_key(password)
    iv = data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(data[16:])
    return unpad(decrypted)
