import argparse
import databaseManager
import fileManager
from config import CONFIG
import client
from aquaError import NotAuthenticatedError

class clientInterface(object):
    def __init__(self, username, password, network, todo,networkPassword, path=None, gui=None,  code=None):
        self.authenticated = None
        self.__username = username
        self.__password = password
        self.__network = network
        self.todo = todo
        if path is not None:
            self.path = path

        if code is not None:
            self.code = code

        self.__networkPassword = networkPassword

        self.dbInterface = databaseManager.dbManager(CONFIG['database']['username'],
                                                     CONFIG['database']['password'],
                                                     CONFIG['database']['host'],
                                                     CONFIG['database']['database'])

        self.authenticated = self.checker()


    def checker(self):
        return self.dbInterface.authenticateUser(self.__username, self.__password, self.__network):

    def analyse(self):
        if not self.authenticated:
            raise NotAuthenticatedError()

        if self.todo == "upload":
            with open(path,"r") as f:
                data = f.read()
            network_info = self.dbInterface.getNetworkInfo(self.__network)
            c, d, f = fileManager.exploder(data, network_info)
            for ip in list(d.keys()):
                tosend = {
                    "network_id": self.__network,
                    "password": self.__networkPassword,
                    "todo": "write_file",
                    "password": self.__networkPassword,
                    "data": d[ip]
                }
                client.send(ip, tosend)

        if self.todo == "retrieve":
            name, hash, nodecode = self.code.split(":") #51152b82-7d5e-42bc-a43e-9897fc5e2eb9:700071f878c6ea354072564be2131b0c:A0-A1-A2-A3-A4-A5-A6-A7-A8
            nodeislist = nodecode.split("-")
            iplist = self.dbInterface.getInfoFromCode(nodelist, self.__network)
            tosend = {
                "network_id": self.__network,
                "password": self.__networkPassword,
                "todo": "read_file",
                "filename": name
            }

if __name__ == '__main__':
    from getpass import getpass
    parser = argparse.ArgumentParser(description="Client interface for the aqua system")
    parser.add_argument("-u", help="Username entry")
    parser.add_argument("-p", help="Mean you are using a password", action='store_true')
    parser.add_argument("-P", help="Path of the file only usefull when uploading file")
    parser.add_argument("-n", help="Network linked to the user")
    parser.add_argument("-np", help="Network password", action='store_true')
    parser.add_argument("-t", help="What you want to do", type=str, choices=["upload", "retrieve"])
    parser.add_argument("-c", help="Retrieve code only usefull when retrieving file")
    args = parser.parse_args()
    if args.p:
        password = getpass("User password :")
    else:
        password = ""

    if args.np:
        networkPassword = getpass("Network password :")


    if args.u and args.t and args.n:
        if args.t == "upload":
            clint = clientInterface(args.u, password, args.n, args.t, networkPassword, path=args.P)

        elif args.t == "retrieve":
            clint = clientInterface(args.u, password, args.t, networkPassword, code=args.c,)

        else:
            raise NotImplementedError("not implemented methode")
