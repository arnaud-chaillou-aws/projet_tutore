import json
from hashlib import md5
from aquaError import AddBeforeNewError

class FileManager(object):

    @staticmethod
    def exploder(data, network_info):
        """
        This function split a given file into equals pieces depending of the lenght of the given network

        Cette fonction transforme un fichier en un dictionnaire de morceau egal en fonction de la taille du reseau qui lui a été fourni
        """
        sums = md5(data.encode()).hexdigest()
        node_list, code_list = network_info # exemple: [0,1,2,3,4,5,6,7,8], ['A0','A1','A2','A3','A4','A5','A6','A7','A8']
        nb_file_to_create = len(node_list)//3
        if len(data) % nb_file_to_create:
            toadd = data[-(len(data)%nb_file_to_create):]
            tosplit = data[:-(len(data)%nb_file_to_create)]
        else:
            toadd = None
            tosplit = data
        listdata = []
        dictdata = {}
        for piece in range (0, len(tosplit), len(tosplit)//nb_file_to_create):
            for i in range (3):
                addeddata = tosplit[piece:piece+len(tosplit)//nb_file_to_create]
                listdata.append({piece: addeddata})
        for d in listdata[-3:]:
            for k in d:
                d[k]=d[k].replace(d[k], d[k] + toadd)

        for i in range(len(node_list)):
            dictdata[node_list[i]] = listdata[i]

        filename = str(uuid4())
        code = filename + ":" + sums + ":"
        for nb, nodeid in enumerate(code_list):
            code += nodeid
            if nb != len(code_list)-1:
                code += "-"
        return code, dictdata, filename

    def createUpdate(self, data):
        """
        take data a return a sendable dictionnary.
        """
        pass

    @staticmethod
    def write(path, data):
        with open(path, "w") as f:
            f.write(data)

    @staticmethod
    def read(path):
        try:
            with open(path, "r") as f:
                data = f.read()

        except FileNotFoundError:
            return None

        return data

class fileMaker(object):
    def __init__(self):
        try:
            with open("/tmp/.filelist","r") as f:
                self.filelist = json.loads(f.read())

        except FileNotFoundError:
            self.filelist = dict()
            with open("/tmp/.filelist","w") as f:
                f.write(json.dumps(self.filelist))

    def add(self, filename, data):
        if not self.isin(filename):
            self.new(filename)
        try:
            with open("/tmp/" + filename, "r") as f:
                mydict = json.loads(f.read())
            mydict[list(data.keys())[0]]= list(data.values())[0]

            if self.checkover(filename, mydict):
                self.filelist.pop(filename)
                with open("/tmp/.filelist","w") as f:
                    f.write(json.dumps(self.filelist))
                return True
            with open("/tmp/" + filename, "w") as f:
                f.write(json.dumps(mydict))
            return False

        except FileNotFoundError:
            raise AddBeforeNewError()

    def checkover(self, filename, dict):
        hash = self.filelist[filename]
        data = str()
        for pieces in sorted(list(dict.keys())):
            data+=dict[pieces]
        if hash == md5(data.encode()).hexdigest():
            with open("/tmp/" + filename, "w") as f:
                f.write(data)
            return True
        return False

    def new(self, filename, hash):
        self.filelist[filename]=hash
        with open("/tmp/" + filename, "w") as f:
            f.write(json.dumps(dict()))

        with open("/tmp/.filelist","w") as f:
            f.write(json.dumps(self.filelist))

    def isin(self, filename):
        if filename in self.filelist:
            return True
        return False
