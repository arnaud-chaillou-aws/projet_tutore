import socket as s
import time
import threading
import base64
import crypto
import rsa
import ssl
import os
import signal
import mysqlcmd
import json

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
	def __init__(self, host, code, data, port = 1337):
		self.port = port
		self.code = code
		self.data = data
		self.aeskey = ""
		self.host = host
		self.csock = s.socket(s.AF_INET, s.SOCK_STREAM)
		try:
			self.csock.settimeout(15)
			self.csock.connect((self.host, self.port))
		except:
			print("can't connect to destination %s on port %d" % (self.host, 1337))
			#os.killpg(os.getpid(), signal.SIGTERM)
		self.setuptls()
		self.send()

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

	def send(self):
		ssender(json.dumps({"code": self.code, "data": self.data}), self.csock, self.aeskey)

	def askpid(self):
		ssender(1, self.csock, self.aeskey)
		pid = sreciever(self.csock, self,aeskey)
		return pid

class Serveur(object):
	def __init__(self, port = 1337):
		self.aeskey = ""
		self.port = port
		self.ssock = s.socket(s.AF_INET, s.SOCK_STREAM)
		self.serveur()

	def serveur(self):
		while (1):
			try:
				self.ssock.bind(('', self.port))
			except:
				break
			self.ssock.listen(20)
			while (1):
				(conn, (ip, port)) = self.ssock.accept()
				newthread = threading.Thread(target = self.reception(conn))


	def reception(self, conn):
		self.setuptls(conn)
		self.receiv(conn)

	def working(self, conn, code, data):
		if code == 1: #service stop
			pid = os.getpid()
			print("1")
			ssender(pid, conn, self.aeskey)
			print("2")

		elif code == 2: #Join network
			#data = sreciever(conn, self.aeskey) #reception data
			data = data.loads(data) #transformation des data en dictionaire
			select1 = {
				'network': data["id_reseau"]
			}
			rep1 = mysqlcmd.selectall(select1, mysqlcmd.noeud).count()
			select2 = {
				'network_id': data["id_reseau"]
			}
			tmp = mysqlcmd.select(select2, mysqlcmd.networks)
			rep2 = tmp.maxnode
			if rep1 < rep2: #si il y a moins de noeuds que le maximum
				hasher = crypto.Hash()
				hpassword = hasher.pbkdf2(data["password"])
				if hpassword == tmp.network_password:
					ssender(1, conn, self.aeskey)
					tmp4 = 1
					tmp = 1
					tmp2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
					tmp3=tmp2[0]
					for i in range (0,rep1,1):
						tmp4+=1
						if tmp4 == 10:
							tmp3 = tmp2[tmp]
							tmp+=1
							tmp4=0
					code = tmp3+str(tmp4)
					insertor = {
						'sonde_ip': data["ip"],
						'sonde_id': code,
						'network': data["id_reseau"],
						'nb_files': 0
						}
					mysqlcmd.insert(insertor, mysqlcmd.noeud)
				else:
					ssender(2, conn, self.aeskey)
			else:
				ssender(2, conn, self.aeskey)

		elif code == 3: #ping
			print("ping")
			conn.close()

	def receiv(self, conn):
		rep = json.loads(sreciever(conn, self.aeskey))
		code = rep['code']
		data = rep['data']
		self.working(conn, code, data)

	def setuptls(self, conn):
		ownpub = crypto.keys.pubkey
		ownpriv = crypto.keys.privkey
		friendn = reciever(conn)
		friende = reciever(conn)
		sender(str(ownpub.n), conn)
		sender(str(ownpriv.e), conn)
		self.friendpub = rsa.key.PublicKey(int(friendn),int(friende))
		ecpk = reciever(conn)
		cpk = rsa.decrypt(ecpk.encode('iso-8859-1'), ownpriv)
		spk = ssl.RAND_bytes(16)
		espk = rsa.encrypt(spk, self.friendpub)
		sender(espk.decode('iso-8859-1'), conn)
		self.aeskey = cpk + spk

class HelpMe():
	def __init__(self):
		self.Serveur = ("Object serveur, accept toute les communication fait pour communiquer avec l'objet client utilise les fonctions/methodes sender, reciever, ssender, ssreceiver, setuptls")
		self.Client = ("Object client, se connect à un serveur nécessite une ip se connecte au port 1337 par default utilise les fonction/methode sender, reciever, ssender, ssreceiver, setuptls")
		self.sender = ("Met en forme un paquet et l'envoie nécessite une data à envoyer et un socket")
		self.reciever = ("Attend, recoit et remet en forme un paquet nécessite un socket")
		self.ssender = ("Identique a sender mais utilise un chiffrement aes via une clée établie par la methode setuptls et fourni en parametre")
		self.sreciever = ("Identique a reciever mais dechiffre de l'aes via une cléeetablie par la methode setuptls et fourni en parametre")
		self.setuptls = ("methodes présente dans les classes Serveur et Client permet de définir une clée aes unique a chaque echange client/serveur")

	def __str__(self):
		return ("Classes/Methodes/focntions expliqué: Serveur, Client, sender, reciever, ssender, sreciever, setuptls")
