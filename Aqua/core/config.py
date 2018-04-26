from twisted.python import log
import sys
import configparser

class Colorized(log.FileLogObserver):
    def emit(self, eventDict):
        self.write("\033[3m")
        if eventDict["isError"]:
            self.write("\033[91m") #Rouge

        if not eventDict["isError"]:
            self.write("\033[92m") #Bleu

        log.FileLogObserver.emit(self, eventDict)

OBSERVER = Colorized(sys.stdout)

CONFIG = configparser.ConfigParser()
CONFIG.read('/home/arnaud/projet_tutore/v4/server.config')

"""
Use Exemple :

from setuplog import OBSERVER

log.addObserver(OBSERVER.emit)

log.msg("Starting log")

try:
    1/0
except ZeroDivisionError as e:
    log.err(e)

log.msg("Ending")
"""
