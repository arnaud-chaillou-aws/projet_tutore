from sqlobject import *
from binascii import hexlify
import hashlib

class User(SQLObject):
    username = StringCol()
    password = StringCol(length=128)
    network = ForeignKey('network_id')

    @staticmethod
    def insert(username, password, network_info):
        s = User.searchUser(username)
        network_id, password = network_info
        network = Network.searchNetwork(network_id, password)

        if len(list(s)) == 0 and network is not None:
            new = User(
                username=username,
                password=_hashme(password),
                network = network
            )
            return new
        return None

    @staticmethod
    def checkUser(username, password, network):
        s = User.select(
            AND(
                User.q.username == username,
                User.q.password == _hashme(password),
                User.q.network == network
            )
        )
        if len(list(s)) == 1:
            return True
        return False

    @staticmethod
    def searchUser(username):
        s = User.select(
            AND(
                User.q.username == username,
            )
        )
        return s

class Network(SQLObject):
    network_id = StringCol()
    password = StringCol()
    max_agent = IntCol()

    @staticmethod
    def insert(network_id, password, max_agent):
        s = Network.searchNetwork(network_id)
        if len(list(s)) == 0:
            new = Network(
                network_id=network_id,
                password=_hashme(password),
                max_agent=max_agent
            )
            return new
        return None

    @staticmethod
    def listNetworkMember(network_id):
        s = Network.select(
            AND(
                Network.q.network_id == network_id,
            )
        )
        return list(s)

    @staticmethod
    def checkNetwork(network_id, network_password):
        s = Network.select(
            AND(
                Network.q.network_id == network_id,
                Network.q.password == network_password,
            )
        )
        if len(list(s)) == 1:
            return True
        return False

    @staticmethod
    def canAdd(network_id):
        s = Network.select(
            AND(
                Network.q.network_id == network_id
            )
        )
        if len(list(s)) == 1:
            if s.max_agent < len(Network.listNetworkMember(network_id)):
                return True
            return False
        return False

    @staticmethod
    def searchNetwork(network_id, password):
        s = Network.select(
            AND(
                Network.q.network_id == network_id,
                Network.q.password == password,
            )
        )
        if len(list(s)) == 1:
            return s[0]
        return None

class Node(SQLObject):
    node_id = StringCol()
    node_ip = StringCol()
    network = StringCol()

    @staticmethod
    def insert(node_id, node_ip, network):
        if Node.checkNode(node_ip, network):
            return False
        Node(
            node_id=node_id,
            node_ip=node_ip,
            network=network
        )
        return True

    @staticmethod
    def searchNode(network):
        s = Node.select(
            AND(
                Node.q.network == network,
            )
        )
        return s.count(), list(s)

    @staticmethod
    def checkNode(node_ip, network):
        s = Node.select(
            AND(
                Node.q.network == network,
                Node.q.node_ip == node_ip
            )
        )
        if len(list(s)) != 0:
            return 1
        return 0

    @staticmethod
    def searchAllNode():
        s = Node.select()
        return s.count(), s

    @staticmethod
    def findNode(code, network):
        s = Node.select(
            AND(
                Node.q.node_id == code,
                Node.q.network == network
            )
        )
        if len(list(s)) == 1:
            return list(s)[0]
        return None
    
def _hashme(password):
    salt = hashlib.sha256(password.encode()).hexdigest()
    return hexlify(hashlib.pbkdf2_hmac('sha512',
                                        password.encode(),
                                        salt.encode(),
                                        100000)).decode()

def init(username, password, host, database):
    sqlhub.processConnection = connectionForURI('mysql://%s:%s@%s/%s' % (username, password, host, database))
    Node.createTable(ifNotExists=True)
    Network.createTable(ifNotExists=True)
    User.createTable(ifNotExists=True)

# a = init("root","root","localhost","em2a")
# nb, a = Node.searchNode("test")
# print("il y a", nb)
