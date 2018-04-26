import sys
import OpenSSL

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, ssl, defer
from twisted.python import log

from config import OBSERVER

# from em2a import em2a

log.addObserver(OBSERVER.emit)

class em2aServer(Protocol):
    def __init__(self):
        self.buffer = bytes()
        self.peerinfo = str()

    def connectionMade(self):
        self.peerinfo = self.transport.getPeer()

    def dataReceived(self, data):
        self.buffer += data

    def connectionLost(self, reason):
        """
        Créer une fonction qui retour un deferred avec tout les bon callback (UserInterface) puis je fire le callback
        """
        d = self.handler()
        reactor.callLater(0, d.callback, None)

    def handler(self):
        if self.contentChecker():
            todo =  self.buffer["todo"]
            d = defer.Deferred()
            self.infoRetriever(self, todo, d)
            d.addErrback(log.err)
        return d

    def contentChecker(self):
        if isinstance(self.buffer, dict):
            return True
        return False

    def infoRetriever(self, todo):
        try:
            network_id = self.buffer["network_id"]
            password = self.buffer["password"]
            if todo == "write_file":
                data = self.buffer["data"]
                name = self.buffer["filename"]
                networkInterface = networkManager(network_id, password)
                if networkInterface.authenticate:
                    networkInterface.write(data, name)
                return

            elif todo == "read_file":
                filename = self.buffer["filename"]
                networkInterface = networkManager(network_id, password)
                if networkInterface.authenticate:
                    data = networkInterface.read(filename)
                    if data is not None:
                        tosend = {
                            "todo": "retrieve",
                            "filename": filename,
                            "data": data
                        }
                        em2aClient.send(self.peerinfo.host, tosend)
                return

            elif todo == "register":
                networkInterface = networkManager(network_id, password)
                if networkInterface.authenticate:
                    if networkInterface.nodeRegister(self.peerinfo.host):
                        tosend, hostlist = networkInterface.DBupdate(todo, self.peerinfo.host)
                        if tosend is not None:
                            for ip in hostlist:
                                em2aClient.send(ip, tosend)

            elif todo == "retrieve":
                filename = self.buffer["filename"]
                data = self.buffer["data"]
                networkInterface = networkManager(network_id, password)
                if networkInterface.authenticate:
                    fm = networkInterface.fileMaker()
                    if fm.add(filename, data):
                        log.msg("A new file as been recreated id:", filename)
                return

            elif todo == "db_update":
                table = self.buffer["target_table"]
                update_info = self.buffer["update_info"]
                networkInterface = networkManager(network_id, password)
                if networkInterface.authenticate:
                    tosend, hostlist = networkInterface.DBUpdate(table, update_info)
                    if tosend is not None:
                        for ip in hostlist:
                            em2aClient.send(ip, tosend)
            return

        except KeyError:
            return

class em2aFactory(Factory):
    # protocol = em2aServer

    def buildProtocol(self, addr):
        proto = em2aServer()
        proto.factory = self
        return proto


def main():
    cert_path = '/home/arnaud/projet_tutore/v4/core/certfile/certificate.pem'
    key_path = '/home/arnaud/projet_tutore/v4/core/certfile/key.pem'
    ssl_context = ssl.DefaultOpenSSLContextFactory(key_path, cert_path)
    reactor.listenSSL(12345, em2aFactory(), ssl_context)
    reactor.run()

if __name__ == '__main__':
    main()
