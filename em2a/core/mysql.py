from sqlobject import *
from binascii import hexlify
import hashlib

class User(SQLObject):
    username = StringCol()
    password = StringCol(length=128)

    @staticmethod
    def insert(username, password):
        s = User.searchUser(username)
        if len(list(s)) == 0:
            new = User(
                username=username,
                password=_hashme(password)
            )
            return new
        return None

    @staticmethod
    def checkUser(username, password):
        s = User.select(
            AND(
                User.q.username == username,
                User.q.password == _hashme(password),
            )
        )
        if len(list(s)) == 1:
            return s
        return None
    @staticmethod
    def searchUser(username):
        s = User.select(
            AND(
                User.q.username == username,
            )
        )
        return s

class Network(SQLObject):
    em2a_id = StringCol()
    password = StringCol()
    max_agent = IntCol()

    @staticmethod
    def insert(em2a_id, password, max_agent):
        s = Network.searchNetwork(em2a_id)
        if len(list(s)) == 0:
            new = Network(
                em2a_id=em2a_id,
                password=_hashme(password),
                max_agent=max_agent
            )
            return new
        return None

    @staticmethod
    def searchNetwork(em2a_id):
        s = Network.select(
            AND(
                Network.q.em2a_id == em2a_id,
            )
        )
        return s[0]

    @staticmethod
    def checkNetwork(network_id, network_password):
        s = Network.select(
            AND(
                Network.q.em2a_id == network_id,
                Network.q.password == network_password,
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

        new = Node(
            node_id=node_id,
            node_ip=node_ip,
            network=network
        )
        return new

    @staticmethod
    def searchNode(network):
        s = Node.select(
            AND(
                Node.q.network == network,
            )
        )
        return s.count(), s

    @staticmethod
    def searchAllNode():
        s = Node.select()
        return s.count(), s

def _hashme(password):
    salt = hashlib.sha256(password.encode()).hexdigest()
    return hexlify(hashlib.pbkdf2_hmac('sha512',
                                        password.encode(),
                                        salt.encode(),
                                        100000)).decode()

def init(username, password, host, database):
    sqlhub.processConnection = connectionForURI('mysql://%s:%s@%s/%s' % (username, password, host, database))
    try:
        Node.createTable()
    except:
        pass
    try:
        Network.createTable()
    except:
        pass
    try:
        User.createTable()
    except:
        pass

# a = init("root","root","localhost","em2a")
# nb, a = Node.searchNode("test")
# print("il y a", nb)
