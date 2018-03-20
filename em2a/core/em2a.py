"""
Em2a server
"""
import base64
import uuid
import mysql

from random import randrange
from config import CONFIG

from sys import exit
from Crypto.Cipher import AES
from hashlib import md5

import client

class FileWorker(object):
    """
    The role of this class is to handle every operation that we might need to do on a file

    Cette classe a pour role de s'occuper de toute les taches nécessaire pour le traitement de fichier
    """
    class AESCipher(object):
        """
        This inner class add a AES support to the FileWorker class

        Cette classe interne ajoute des option de chiffrement AES a nore classe FileWorker
        """
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

        def _unpad(self, s):
            return s[:-ord(s[len(s)-1:])]

        def _pad(self, s):
            return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def exploder(self, data, network_id):
        """
        This function split a given file into equals pieces depending of the lenght of the given network

        Cette fonction transforme un fichier en un dictionnaire de morceau egal en fonction de la taille du reseau qui lui a été fourni
        """
        node_list, code_list = DBWorker.getNodeList(network_id)
        nb_file_to_create = len(node_list)//3
        if len(data) % nb_file_to_create:
            toadd = data[-(len(data)%nb_file_to_create):]
            tosplit = data[:-(len(data)%nb_file_to_create)]
        else:
            toadd = None
            tosplit = data
        listdata = []
        dictdata = {}
        for piece in range (0, len(tosplit), len(tosplit)//nb_file_to_create):
            for i in range (3):
                addeddata = tosplit[piece:piece+len(tosplit)//nb_file_to_create]
                if piece == (len(tosplit)//nb_file_to_create) and toadd:
                    addeddata += toadd
                listdata.append(addeddata)
        for i in range(len(node_list)):
            dictdata[node_list[i]] = listdata[i]

        fileid = str(uuid.uuid4())
        code = fileid + ":"
        for nodeid in code_list:
            code += nodeid
        return code, dictdata, fileid

    def writer(self, name, data):
        """
        Write the given data to a file as the given name.

        Ecrit les données fourni dans un fichier nommé dans le nom donnée.
        """
        try:
            with open(CONFIG.get('backend', 'savepath')+name, "a") as file:
                file.write(data)

        except PermissionError as e:
            log.err("Savepath option pointe vers un repertoire non autorisé", e)
            exit(1)

    def reader(self, path):
        """
        Read a file and return he's content

        Lis un fichier et retourne sont contenu
        """
        try:
            with open(path, r) as file:
                data = file.read()

        except PermissionError as e:
            log.err("Le fichier le peut pas être lu", e)
            exit(1)

        except FileNotFoundError as e:
            log.err("Le fichier n'existe pas", e)
            exit(1)
        return data

class DBWorker(object):
    def __init__(self):
        self.__username = CONFIG.get('MySQL', 'username')
        self.__password = CONFIG.get('MySQL', 'password')
        self.__host = CONFIG.get('MySQL', 'host')
        self.__database = CONFIG.get('MySQL', 'database')

        mysql.init(self.__username, self.__password, self.__host, self.__database)

    def decentralization(self, update, network_id, network_password, table):
        CltInterface = ClientInterface(network_id, network_password)
        nb, nodes = self.getNodeUpdate(network_id)
        hostlist = []
        for node in list(network_id):
            hostlist.append(node.node_ip)
        CltInterface.send("database", update, network_id, network_password, table=table) #(self, subject, data, hostlist=None, filename=None):

    def createNetwork(self, password, max_agent):
        em2a_id = str(uuid.uuid4())
        if mysql.Network.insert(em2a_id, password, max_agent) is None:
            return 1, None
        return 0, em2a_id

    def createUser(self, username, password, network_id, network_password, share=True):
        if self.getNetwork(network_id, network_password):
            return 2
        new_user = mysql.User.insert(username, password)
        if new_user is None:
            return 1
        if share:
            decentralization((username, password), network_id, network_password, "User")
        return 0

    def createNode(node_ip, network_id):
        nb, val = self.getNodeUpdate(network_id)
        dictionnaire = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
        b = nb//26
        a = dictionnaire[b]
        c = nb-(26*b)
        node_id =  str(a) + str(c)
        return 0

    # def joinNetwork(self, side):
    #     if side == 0: #joiner
    #         client.send(..)
    #     elif side == 1: #reciever

    def getNodeList(self, network_id):
        nb, inf = mysql.Node.searchNode(network_id)
        iplist = []
        idlist = []
        for i in range(nb):
            idlist.append(inf[i].node_id)
            iplist.append(inf[i].node_ip)
        while (len(iplist) % 3 != 0):
            delete = randrange(len(iplist))
            iplist.pop(delete)
            idlist.pop(delete)
        return iplist.sort(), idlist.sort()

    def getNodeUpdate(self, network_id):
        return mysql.Node.searchNode(network_id)

    def getUser(self, username, password):
        return mysql.checkUser(username, password)

    def getNetwork(self, network_id, password):
        if mysql.checkNetwork(network_id, password) is None:
            log.err("Wrong creds for network", network_id)
            return 1
        log.msg("Authentification succed for", network_id)
        return 0

class ServerInterface(object):
    def receivedBuffer(self, buffer, peerinfo):
        if self.checkAuth(buffer, peerinfo):
            return

        if buffer["subject"] == "file":
            log.msg("")
            Fileworker.write(buffer["filename"], buffer["data"])

        elif buffer["subject"] == "database":
            if buffer["table"] == "User":
                dbconn = DBWorker()
                dbconn.createUser(buffer["data"][0], buffer["data"][1], buffer["network_id"], buffer["network_password"], share=False)

            elif buffer["table"] == "Node":
                pass

    def checkAuth(self, data, peerinfo):
        try:
            network_id = data["network_id"]
            network_password = data["network_password"]
            dbconn = DBWorker()
            if dbconn.getNetwork(network_id, network_password):
                log.err("Wrong peer", peerinfo)
                return 1
            log.msg("Good peer")
            return 0

        except KeyError:
            log.err("Wrong peer", peerinfo)
            return 1

class ClientInterface(object):
    def __init__(self, network_id, network_password):
        self.network_id = network_id
        self.network_password = network_password

    def send(self, subject, data, hostlist=None, filename=None, table=None):
        if subject == "file":
            for host in data:
                to_send = {
                    "subject": subjet,
                    "network_id": self.network_id,
                    "network_password": self.network_password,
                    "data": data[host],
                    "filename": filename
                }
                client.send(host, to_send)

        elif subject == "database":
            for host in hostlist:
                to_send = {
                    "subject": subjet,
                    "network_id": self.network_id,
                    "network_password": self.network_password,
                    "data": update,
                    "table": table,
                }
                client.send(host, to_send)

        else:
            log.err("Unsuported request")
            exit(1)

class UserInterface(object):
    def __init__(self, username=None, password=None):
        if username == None or password == None:
            authentification()
        self.user = DBWorker.getUser(username, password)

    def sendFile(self, path, network_id, network_password, encrypt=True):
        if not self.user:
            log.err("You must be logged to use this method")
            return 1

        if DBWorker.getNetwork(network_id, network_password) is None:
            log.err("Wrong password")
            return 1

        data = FileWorker.reader(path)

        if encrypt:
            cipher = FileWorker.AESCipher(md5(self.user.password.encode).hexdigest())
            data = cipher.encrypt(data)

        code, ready_to_send_dict, filename = FileWorker.exploder(data, network_id)

        interface = ClientInterface(network_id, network_password, filename)
        interface.send("file", ready_to_send_dict)

        return code

    def createUser(self, username, password, network_id, network_password):
        if not self.user:
            log.err("You must be logged to use this method")
            return 1

        log.msg("Called createUser by", self.user)
        dbintf = DBWorker()
        status = dbintf.createUser(username, password, network_id, network_password)

        if status == 1:
            log.err("Username already taken")
            return 1

        elif status == 2:
            log.err("Wrong network informations")
            return 1

        elif status == 0:
            log.msg("Username created", username, password)
            return 0

        else:
            log.err("Unsuported operation. status =", status)
            return 1

    def createNetwork(self, password, max_agent=50):
        if not self.user:
            log.err("You must be logged to use this method")
            return 1

        dbconn = DBWorker()
        status, id = dbconn.createNetwork(password, max_agent)

        if status:
            log.err("Erreur lors de la création du réseau")
            return None


        log.msg("Nouveau réseau créé id:{} par {}".format(id, self.user))
        return id

    def joinNetwork(self, si, network_id, network_password, iplist):
        if not self.user:
            log.err("You must be logged to use this method")
            return 1

        log.msg("Join network used by", self.user)
        dbconn = DBWorker()
        if dbconn.getNetwork(network_id, network_password):
            log.err("Wrong creds for network", network_id)
            return 1

        for ip in iplist:
            status = dbconn.createNode(ip, network_id)
            if not status:
                log.msg("New node add to {} with the ip {}".format(network_id, ip))
            else:
                log.err("Unsuported return for joinNetwork methode", status)
