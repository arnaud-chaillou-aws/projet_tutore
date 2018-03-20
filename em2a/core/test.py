from twisted.internet.defer import Deferred
from twisted.python import log, failure
from twisted.internet import reactor
from setuplog import OBSERVER
from twisted.internet.task import LoopingCall
import time

log.addObserver(OBSERVER.emit)

log.msg("Starting log")

class MyError(Exception):
    def __init__(self, tuple):
        Exception.__init__(self)
        self.msg, self.entry = tuple

    def __str__(self):
        return self.msg

def printer(argument):
    print(argument)

def createdefer(entry):
    d = Deferred()
    d.addCallback(func1).addCallback(func2)
    return d

def func1(entry):
    raise MyError(("hehe", entry))
    return entry + 1

def func2(result):
    return result*2

def losecon(buff):
    d = createdefer(buff)
    d.addCallbacks(log.msg, log.err)
    d.callback(1)

reactor.callLater(1, losecon, 1)
reactor.run()
