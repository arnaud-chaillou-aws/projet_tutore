import uuid

from random import randrange
from config import CONFIG

import mysql
import client


class em2a(object):
    def __init__(self):
        self.__username = CONFIG.get('MySQL', 'username')
        self.__password = CONFIG.get('MySQL', 'password')
        self.__host = CONFIG.get('MySQL', 'host')
        self.__database = CONFIG.get('MySQL', 'database')

        mysql.init(self.__username, self.__password, self.__host, self.__database)

    def reciever(self, data):
        if data[0]:
            self.recvupate(data) #it's a dbupdate
        else:
            self.recvfile(data) #its a file


    def _get_node(self, network_id):
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

    def sendfile(self, file_info):
        ntwid, path = file_info
        node_list, code_list = self._get_node(ntwid)
        data = _get_data(path)
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
        for key in dictdata:
            client.send(key, (1, fileid, dictdata[key]))
        code = fileid + ":"
        for nodeid in code_list:
            code += nodeid
        return code

    def recvfile(self, buffer):
        """
        Add a file to the system in the repertory choosen in the config file, must be called with a instance of em2a, and a tuple containing the name of the file as [0] and the data as [1].

        Ajoute un fichier au systeme dans le repertoire choisie via le fichié de config, pour être appellée cette methode a besoin d'une instance de em2a et un tuple avec le nom du fichier à [0]
        et les data à [1].
        """
        code, filename, data = buffer
        with open(CONFIG.get('backend', 'savepath')+filename, "a") as file:
            file.write(data)

    def newuser(self, username, password):
        """
        Try to add a user to the local database, if it work send the update to the nodes, must be called with a instance of em2a, a username and a password.

        Essaye d'ajouter un utilisateur a la base de donnée local, si c'est possible alors envoie une mise a jour aux noeuds, pour appeller cette focntion vous devez fournir une instance de em2a
        l'identifiant et le mot de passe d'un utilisateur
        """
        new = mysql.User.insert(username, password)
        if new is not None:
            nb, r = mysql.Node.searchAllNode()
            node_list=[]
            for i in range(nb):
                node_list.append(r[i].node_ip)
            node_list = list(set(node_list))
            em2a.sendupdate(node_list, 0, (username, password))
            return 0
        else :
            return 1

    def newnetwork(self, password, max_agent=50):
        """
        Try to add a network to the local database, return the the info generated wich contain the network_id, must be called with a instance of em2a and a password for the network
        and eventually the number of node maximum for the network wich is 50 by default.

        Essaye d'ajouter un reseau a la base de donnée local, retourne toutes les info concernant le reseau notament l'id network, doit être appellé avec une instance de em2a et un mot de passe
        si il n'est pas precisé le nombre de noeuds maximum de ce reseau sera 50.
        """

        new = mysql.Network.insert(network_id, password, max_agent)
        if not new:
            return 0

        return new

    def joinnetwork(self, host, password):
        client.send()

    @staticmethod
    def sendupdate(hostlist, table, data):
        for ip in hostlist:
            client.send(ip, (0, (table, data)))
        return data

    def recvupate(self, data):
        code, (table, updateInfo) = data
        if table == 0: #User
            n = mysql.User.insert(updateInfo[0], updateInfo[1])
            if n is not None:
                return 0
            else:
                return 1

        elif table == 1:
            pass


def _get_data(path):
    with open(path, "r") as file:
        data = file.read()
    return data
