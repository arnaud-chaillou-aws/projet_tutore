import hashlib
from time import time
import mysqlcmd
import json
import communication

class blockchain(initialisateur):
    def __init__(self, networkid):
        self.chain = getchain()
        self.new_data = [{'networks': 'primordial'}, {'noeud': 'primordial'}, {'users': 'primordial'}]
        self.node = self.getnode(networkid)
        self.new_block(previous_hash=0)

    def new_block(self, previous_hash = None, new_data = None):

        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'update': new_data or self.new_data,
            'node': self.node,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        if previous_hash = 0:
            self.send_block(block)

    def send_block(self, block):
        block = block.dumps(block).encode()


    def recv_block(self, block):
        pass

    def hash(self, block):
        encdata = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encdata).hexdigest()

class initialisateur:
    def getchain(self):
        output = []
        selector = {'forselector': 0}
        chain = mysqlcmd.selectall(selector, mysqlcmd.Hash)
        chain = chain.orderBy('numero')
        if chain.count == 0:
            return output
        for x in range (chain.count()):
            if chain[x].numero == x:
                output.append(chain[x].val_hash)
        return output

    def getnode(self, id):
        output = []
        selector = {'network': id}
        chain = mysqlcmd.selectall(selector, mysqlcmd.noeud)
        chain = chain.orderBy('id')
        if chain.count() == 0:
            raise SystemError("Il n'y a aucun noeud dans ce réseau")
        for x in range (0, chain.count(), 1):
            print(x, chain.count())
            if chain[x].id == x+1:
                if test(chain[x].sonde_ip) == True:
                    output.append(chain[x].sonde_ip)
        return output

def test(ip):
    try:
        clt = communication.Client(ip)
        communication.ssender('\x03', clt.csock, clt.aeskey)
        return True
    except:
        return False
