import socket as s
import threading
import base64
import crypto
import rsa
import ssl
import os
import signal
import mysqlcmd

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
	def __init__(self, host):
		print("ici")
		self.port = 1337
		self.aeskey = ""
		self.host = host
		print("la")
		self.csock = s.socket(s.AF_INET, s.SOCK_STREAM)
		print("lala")
		try:
			print("hihi")
			self.csock.settimeout(15)
			self.csock.connect((self.host, self.port))
			print("connexion réussi")
		except:
			print("hoho")
			print("can't connect to destination %s on port %d" % (self.host, 1337))
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
				self.ssock.bind(('', self.port))
			except:
				break
			self.ssock.listen(20)
			while (1):
				(self.conn, (ip, port)) = self.ssock.accept()
				newthread = threading.Thread(target = self.reception())


	def reception(self):
		self.setuptls()
		self.securesynack()
		self.waiting()

	def waiting(self):
		commande = sreciever(self.conn, self.aeskey)
		if commande == '\x01': #service stop
			pid = os.getpid()
			ssender(pid, self.conn, self.aeskey)

		elif commande == '\x02': #Join network
			data = sreciever(self.conn, self.aeskey) #reception data
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
					ssender("\x01", self.conn, self.aeskey)
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
					ssender("\x02", self.conn, self.aeskey)
			else:
				ssender("\x02", self.conn, self.aeskey)
		elif commande == '\x03': #ping
			self.conn.close()

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
