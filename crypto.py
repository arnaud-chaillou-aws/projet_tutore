import hashlib
import binascii
import rsa
import os

def pbkdf2(password):
    bpassword = password.encode("utf-8")
    salt = hashlib.sha256()
    salt.update(bpassword)
    rsalt = salt.hexdigest()
    rsalt = rsalt.encode("utf-8")
    h=hashlib.pbkdf2_hmac('sha512', bpassword, rsalt, 10000)
    tmp = binascii.hexlify(h)
    tmp = tmp.decode()
    return tmp

class Keys():
    def __init__(self):
        self.pubkey = ""
        self.privkey = ""
        self.keycheck()

    def keycheck(self):
        if not os.path.exists("/etc/ema/pubkey.pem") or not os.path.exists("/etc/ema/privkey.pem"):
            print("la")
            self.keygen()
        else:
            print("ici")
            self.keyload()


    def keygen(self):
        pubkey, privkey = rsa.newkeys(2048)
        pubk = open("/etc/ema/pubkey.pem","wb")
        pub = rsa.PublicKey.save_pkcs1(pubkey, format = 'PEM')
        pubk.write(pub)
        pubk.close()

        privk = open("/etc/ema/privkey.pem","wb")
        priv = rsa.PrivateKey.save_pkcs1(privkey, format = 'PEM')
        privk.write(priv)
        privk.close()

    def keyload(self):
        pubk = open("/etc/ema/pubkey.pem","rb")
        pub = pubk.read()
        self.pubkey = rsa.PublicKey.load_pkcs1(pub, format = 'PEM')

        privk = open("/etc/ema/privkey.pem", "rb")
        priv = privk.read()
        self.privkey = rsa.PrivateKey.load_pkcs1(priv, format = 'PEM')

keys = Keys()
#keycheck()
if __name__ == "__main__":
    print(keys)
