from config import CONFIG
from string import ascii_uppercase

class nodeManager(object):
    """
    Here is a class that describe every function that a nodeManager shoudl have
    """
    def createRepertory(self, directory_name):
        from os import makedirs
        makedirs(CONFIG[server]['dl_path']+directory_name)

    @staticmethod
    def genName(member_number):
        dictionnaire = list(ascii_uppercase)
        if member_number >= 10*len(dictionnaire):
            return None
        a = dictionnaire[member_number//10]
        b = str(member_number%10)
        return  a + b

    def addNode(self, members_count, network):
        node_id = nodeManager.genName(members_count)
        if node_id is not None:
            self.createRepertory(network)
            return True, node_id
        return False, None
