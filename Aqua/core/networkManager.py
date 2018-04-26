"""
This class provide all the logic for a networkManager, u shall inerit you networkManager from this class

a networkManager call must be the only entity to interact with interface
"""
from config import CONFIG

import NodeManager
import UserManagers
import generator
import fileManager
import databaseManager
from aquaError import NotAuthenticatedError

class NetworkManager(object):
    """
    Here a basic NetworkManager
    """
    authenticate = False
    def __init__(self, network, password):
        self.fileMaker = fileManager.fileMaker
        self.network = network
        self.password = password
        self.databaseInterface = databaseManager.dbManager(CONFIG['database']['username'],
                                                           CONFIG['database']['password'],
                                                           CONFIG['database']['host'],
                                                           CONFIG['database']['database'])
        self.authenticate = databaseInterface.authenticateNetwork(self.network, self.password)

    def write(self, data, filename):
        if not self.authenticate:
            raise aquaError.NotAuthenticatedError()

        fileManager.write(CONFIG['server']['dl_path']+ self.network + "/" + filename, data)

    def read(self, filename):
        if not self.authenticate:
            raise aquaError.NotAuthenticatedError()

        return fileManager.read(CONFIG['server']['dl_path']+self.network+ "/" + filename)

    def nodeRegister(self, host):
        if not self.authenticate:
            raise aquaError.NotAuthenticatedError()

        if not self.databaseInterface.canAdd(self.network):
            return False

        members_count, members = self.databaseInterface.listNetworkMember(self.network)

        self.hostlist = list()

        for node in members:
            if node.node_ip == host:
                return False
            self.hostlist.append(node.node_ip)

        status, self.node_id = self.nodeManager.addNode(members_count, self.network):
        if status:
            self.databaseInterface.addNode(self.node_id, host, self.network)
            return True
        return False

    def DBUpdate(self, todo, info):
        if todo == "register":
            tosend = {
                "todo": "db_update",
                "target_table": "Node",
                "update_info": {
                        "node_id": self.node_id,
                        "node_ip": info,
                        "network": self.network
                    }
            }
            return tosend, self.hostlist

        else:
            return None, None
