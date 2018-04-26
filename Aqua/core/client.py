import sys

from twisted.python import log
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, ssl
import OpenSSL
from config import OBSERVER


class ClientProtocol(Protocol):
    """
    Our protocol class.
    """
    def __init__(self, data):
        self.data = data

    def connectionMade(self):
        self.transport.write(self.data)
        self.transport.loseConnection()

class ClientFactory(ClientFactory):
    """
    Our Factory class.
    """
    def __init__(self, data):
        self.data = data

    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        return ClientProtocol(self.data)

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        reactor.stop()

class contextFactory(ssl.ClientContextFactory):
    """
    This class generate and return a SSL context for the Factory
    """
    def getContext(self):
        return OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)

def send(host, data):
    reactor.connectSSL(host, 12345, ClientFactory(data), contextFactory())
    reactor.run()

if __name__ == '__main__':
    log.addObserver(OBSERVER.emit)
    a = send('localhost', 'test'.encode())
