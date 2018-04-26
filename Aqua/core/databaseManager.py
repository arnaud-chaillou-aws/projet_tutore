"""
This class provide the logic to all database manager class

A databaseManager class shall handle every type of request to a database connector
"""
import mysql
from twisted.python import log
from config import OBSERVER

log.addObserver(OBSERVER)

class dbManager(object):
    def __init__(self, username, password, host, database):
        mysql.init(username, password, host, database)

    def authenticateUser(self, username, password, network):
        log.msg("authenticateUser user with %s:%s on network %s" % (username, password, network))
        return mysql.User.checkUser(username, password, network)

    def authenticateNetwork(self, network, creds):
        log.msg("authenticateNetwork used with %s:%s" % (network, creds))
        return mysql.Network.checkNetwork(network, creds)

    def listNetworkMember(self, network):
        return mysql.Node.searchNode(network)

    def addNode(self, node_id, node_ip, network):
        return mysql.Node.insert(node_id, node_ip, network)

    def canAdd(self, network):
        return mysql.Network.canAdd(network)

    def getNetworkInfo(self, network):
        from random import randrange
        c, l = mysql.Node.searchNode()
        iplist = list()
        codelist = list()
        for node in l:
            iplist.append(node.node_ip)
            codelist.append(node.node_ip)

        while(len(iplist) % 3 != 0):
            delete = randrange(len(iplist))
            rip = iplist.pop(delete)
            rip = idlist.pop(delete)

        return (iplist, codelist)

    def getInfoFromCode(self, codelist, network):
        returnlist = list()
        for code in codelist:
            returnlist.append(mysql.Node.findNode(code, network).node_ip)
        return returnlist
