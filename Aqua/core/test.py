from twisted.internet import reactor, defer
from twisted.python import log

def ErrorHandler(failure):
    print(failure)

class server(object):
    def trigger(self):
        self.buffer = [{"a": "b"}]
        d = self.handler()
        reactor.callLater(0, d.callback, None)

    def handler(self):
        d = defer.Deferred()
        d.addCallbacks(self.contentChecker, ErrorHandler)
        return d

    def contentChecker(self, result):
        if isinstance(self.buffer, dict):
            print("ok")
            return True
        raise Exception("n'es pas complet")

a = server()
a.trigger()
reactor.run()
