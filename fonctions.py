import base64
import ssl
import time
import mysqlcmd
import crypto
import sys
import communication
import pickle

def randomname():
    a = str(time.time())
    b = ssl.RAND_bytes(32)
    name = base64.b64encode(a.encode() + b)
    return name.decode()

def createuser(username, password, email):
    secure = crypto.Hash()
    spassword = secure.pbkdf2(password)
    selector = {
        'user': username
    }
    newuser = {
        'user': username,
        'password': spassword,
        'nb_fichier': 0,
        'email': email
    }
    try:
        tmp = mysqlcmd.select(selector, mysqlcmd.users)
        return 2
    except:
        mysqlcmd.insert(newuser, mysqlcmd.users)
        return 0

def createnetwork(password, maxnode): #Création d'un réseau
    network_id = str(randomname())
    self_id = "A1"
    hasher = crypto.Hash()
    ntwpassword = hasher.pbkdf2(password)
    selector = {
        'network_id': network_id
    }
    newnetwork = {
        'self_id': self_id,
        'network_id': network_id,
        'network_master_id': self_id,
        'network_password': ntwpassword,
        'maxnode': maxnode
    }
    newsonde = {
        'sonde_ip': '127.0.0.1',
        'sonde_id': 'A1',
        'network': network_id,
        'nb_files': 0
    }
    try:
        tmp = mysqlcmd.select(selector, mysqlcmd.networks)
        return 2, None
    except:
        mysqlcmd.insert(newnetwork, mysqlcmd.networks)
        mysqlcmd.insert(newsonde, mysqlcmd.noeud)
        return 0, network_id

def joinnetwork(master_ip, id_reseau, password, ip):
    clt = communication.Client(master_ip)
    data = {
        'id_reseau': id_reseau,
        'password': password,
        'ip': ip
    }
    communication.ssender("\x02", clt.cosck, clt.aeskey)
    data = pickle.dumps(data)
    communication.ssender(data, clt.csock, clt.aeskey)
    rep = communication.sreciever(clt.csock, clt.aeskey)
    if rep == "\x02":
        return 2
    else:
        return 0

class HelpMe():
    def __init__(self):
        self.randomname = ("Fonction randomname: retourne une chaine encoder en base64 unique temps en seconde depuis 1970 + 16 random bytes générer aléatoirement")
        self.createuser = ("Fonction createuser: essaye de selectionner un utilisateur dans la base de donnée si il ne réussi pas alors ajoute l'utilisateur via les information entréen paramètre")
        self.createuser = ("Fonction createnetworks: essaye de selectionner un réseau dans la base de donnée si il ne réussi pas alors il ajoute le reseau configurer en tant que master")

    def __str__(self):
        return("Fonction expliqué : randomname, createuser, createnetwork")

if __name__ == "__main__":
    createnetwork(sys.argv[1])
