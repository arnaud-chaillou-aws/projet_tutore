import socket as s
import threading
import base64
import crypto
import rsa
import ssl
import os
import signal

def sender(data, socket):
    data = str(data)
    encoded = data.encode()
    compressed = base64.b64encode(encoded)
    paquet = compressed + b'\n'
    socket.send(paquet)

def reciever(socket):
    buffer = b''
    data = b''
    while data != b'\n':
        buffer += data
        data = socket.recv(1)
    decompressedbuff = base64.b64decode(buffer)
    decoded = decompressedbuff.decode()
    return decoded

def ssender(data, socket, key):
    data = str(data) #je converti en string
    cipher = crypto.AESCipher(key) #je créer l'objet qui me permet de chiffrer
    encrypted = cipher.encrypt(data) #je chiffre mes données grace a mon objet
    spaquet = encrypted.encode() + b'\n' #j'ajoute le signal de fin de message
    socket.send(spaquet) #j'envoie mon paquet sécurisé

def sreciever(socket, key):
    buffer = b''
    data = b''
    while data != b'\n':
        buffer += data
        data = socket.recv(1)
    decoded = buffer.decode()
    cipher = crypto.AESCipher(key)
    decrypted = cipher.decrypt(decoded)
    return decrypted

class Client(object):
    def __init__(self, host, port):
        print("ici")
        self.port = port
        self.aeskey = ""
        self.host = host
        print("la")
        self.csock = s.socket(s.AF_INET, s.SOCK_STREAM)
        print("lala")
        try:
            print("hihi")
            self.csock.connect((self.host, self.port))
            print("connexion réussi")
        except:
            print("hoho")
            print("can't connect to destination %s on port %d" % (dest, 1337))
            #os.killpg(os.getpid(), signal.SIGTERM)
        self.setuptls()
        self.securesynack()

    def setuptls(self):
        ownpub = crypto.keys.pubkey
        ownpriv = crypto.keys.privkey
        sender(ownpub.n, self.csock)
        sender(ownpub.e, self.csock)
        friendn = reciever(self.csock)
        friende = reciever(self.csock)
        self.friendpub = rsa.key.PublicKey(int(friendn),int(friende))
        cpk = ssl.RAND_bytes(16) #création de la client part key
        ecpk = rsa.encrypt(cpk, self.friendpub) #protection de ma partie de la clée avec la clé publique de l'ami
        sender(ecpk.decode('iso-8859-1'),self.csock)
        espk = reciever(self.csock) #encrypted server part key
        spk = rsa.decrypt(espk.encode('iso-8859-1'), ownpriv)
        self.aeskey = cpk + spk

    def securesynack(self):
        ssender("syn", self.csock, self.aeskey)
        rep = sreciever(self.csock, self.aeskey)

    def askpid(self):
        ssender('\x01', self.csock, self.aeskey)
        pid = sreciever(self.csock, self,aeskey)
        return pid

class Serveur(object):
    def __init__(self):
        self.aeskey = ""
        self.port = 1337
        self.ssock = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.serveur()

    def serveur(self):
        while (1):
            try:
                self.ssock.bind(('localhost', self.port))
            except:
                break
                #print("can't setup server on localhost @ %d" % (self.port))
                #os.killpg(os.getpid(), signal.SIGTERM)
            self.ssock.listen(20)
            while (1):
                (self.conn, (ip, port)) = self.ssock.accept()
                newthread = threading.Thread(target = self.reception())


    def reception(self):
        self.setuptls()
        self.securesynack()
        #self.waiting()

    # def waiting(self):
    #     commande = sreciever(self.conn, self.aeskey)
    #     if commande == '\x01':
    #         pid = os.getpid()
    #         ssender(pid, self.conn, self.aeskey)

    def securesynack(self):
        rep = sreciever(self.conn, self.aeskey)
        ssender("ack", self.conn, self.aeskey)

    def setuptls(self):
        ownpub = crypto.keys.pubkey
        ownpriv = crypto.keys.privkey
        friendn = reciever(self.conn)
        friende = reciever(self.conn)
        sender(str(ownpub.n), self.conn)
        sender(str(ownpriv.e), self.conn)
        self.friendpub = rsa.key.PublicKey(int(friendn),int(friende))
        ecpk = reciever(self.conn)
        cpk = rsa.decrypt(ecpk.encode('iso-8859-1'), ownpriv)
        spk = ssl.RAND_bytes(16)
        espk = rsa.encrypt(spk, self.friendpub)
        sender(espk.decode('iso-8859-1'), self.conn)
        self.aeskey = cpk + spk
