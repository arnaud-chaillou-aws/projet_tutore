import hashlib
import sys
import base64
import binascii
import rsa
import os
import ssl
from Crypto.Cipher import AES

def reciever(conn):
    buffer = b''
    data = b''
    while data != b'\n':
        buffer += data
        data = conn.recv(1)
    buffer = base64.b64decode(buffer)
    return buffer.decode()

class Hash(object):
    def __init__(self):
        self.output = ""
        #self.pbkdf2("input")

    def pbkdf2(self, input):
        input = str(input)
        bpassword = input.encode("utf-8")
        salt = hashlib.sha256()
        salt.update(bpassword)
        rsalt = salt.hexdigest()
        rsalt = rsalt.encode("utf-8")
        h=hashlib.pbkdf2_hmac('sha512', bpassword, rsalt, 10000)
        self.output = binascii.hexlify(h)
        self.output = self.output.decode()
        return self.output

class Keys():
    def __init__(self):
        self.pubkey = ""
        self.privkey = ""
        self.keycheck()

    def keycheck(self):
        if not os.path.exists("/etc/ema/pubkey.pem") or not os.path.exists("/etc/ema/privkey.pem"):
            self.keygen()
        else:
            self.keyload()


    def keygen(self):
        self.pubkey, self.privkey = rsa.newkeys(2048)
        pubk = open("/etc/ema/pubkey.pem","wb")
        pub = rsa.PublicKey.save_pkcs1(self.pubkey, format = 'PEM')
        pubk.write(pub)
        pubk.close()

        privk = open("/etc/ema/privkey.pem","wb")
        priv = rsa.PrivateKey.save_pkcs1(self.privkey, format = 'PEM')
        privk.write(priv)
        privk.close()

    def keyload(self):
        pubk = open("/etc/ema/pubkey.pem","rb")
        pub = pubk.read()
        self.pubkey = rsa.PublicKey.load_pkcs1(pub, format = 'PEM')

        privk = open("/etc/ema/privkey.pem", "rb")
        priv = privk.read()
        self.privkey = rsa.PrivateKey.load_pkcs1(priv, format = 'PEM')

class AESCipher(object):
    def __init__(self, key):
        self.bs = 16
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, raw):
        raw = self._pad(raw)
        encrypted = self.cipher.encrypt(raw)
        encoded = base64.b64encode(encrypted)
        return str(encoded, "utf-8")

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        decrypted = self.cipher.decrypt(decoded)
        return str(self._unpad(decrypted), 'utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

keys = Keys()
if __name__ == "__main__":
    key = ssl.RAND_bytes(32)
    print(key)
    cipher = AESCipher(key)
    plaintext = 'ahahah'
    encrypted = cipher.encrypt(plaintext)
    print('Encrypted: %s' % encrypted)
    decrypted = cipher.decrypt(encrypted)
    print('Decrypted: %s' % decrypted)
