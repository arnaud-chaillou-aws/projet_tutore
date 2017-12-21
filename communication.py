import socket as s
import threading
import base64
import crypto
import rsa
import ssl

aeskey = ""

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
    print(key)
    data = str(data) #je converti en string
    cipher = crypto.AESCipher(key) #je créer l'objet qui me permet de chiffrer
    encrypted = cipher.encrypt(data) #je chiffre mes données grace a mon objet
    spaquet = encrypted.encode() + b'\n' #j'ajoute le signal de fin de message
    socket.send(spaquet) #j'envoie mon paquet sécurisé

def sreciever(socket, key):
    print(key)
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
    def __init__(self, port):
        self.port = port
        self.aeskey = ""
        self.client('localhost')

    def client(self, dest):
        self.csock = s.socket(s.AF_INET, s.SOCK_STREAM)
        try:
            self.csock.connect((dest, self.port))
        except:
            print("can't connect to destination %s on port %d" % (dest, 1337))
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
        #print(self.aeskey)

    def securesynack(self):
        ssender("syn", self.csock, self.aeskey)
        rep = sreciever(self.csock, self.aeskey)
        print(rep)

class Serveur(object):
    def __init__(self, port):
        self.aeskey = ""
        self.port = port
        self.ssock = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.serveur()

    def serveur(self):
        while (1):
            try:
                self.ssock.bind(('localhost', self.port))
            except:
                print("can't setup server on localhost @ %d" % (self.port))
            self.ssock.listen(20)
            while (1):
                (self.conn, (ip, port)) = self.ssock.accept()
                newthread = threading.Thread(target = self.reception())

    def reception(self):
        self.setuptls()
        self.securesynack()

    def securesynack(self):
        rep = sreciever(self.conn, self.aeskey)
        ssender("ack", self.conn, self.aeskey)
        print(rep)

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
        #print(self.aeskey)
