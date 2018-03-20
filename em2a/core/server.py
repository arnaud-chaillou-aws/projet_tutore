import sys
import OpenSSL

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, ssl
from twisted.python import log

from setuplog import OBSERVER

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
        backend.reciever(self.buffer, self.peerinfo) #peerinfo.host = ip, peerinfo.port = port, peerinfo.type = type (TCP/UDP)
        """
        Créer une fonction qui retour un deferred avec tout les bon callback (UserInterface) puis je fire le callback
        """
class em2aFactory(Factory):
    protocol = em2aServer

    def buildProtocol(self, addr):
        return em2aServer()


def init():
    cert_path = '/home/arnaud/projet_tutore/v2/em2a/core/certfile/certificate.pem'
    key_path = '/home/arnaud/projet_tutore/v2/em2a/core/certfile/key.pem'
    ssl_context = ssl.DefaultOpenSSLContextFactory(key_path, cert_path)
    reactor.listenSSL(12345, em2aFactory(), ssl_context)
    reactor.run()

init()
