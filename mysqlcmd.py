from sqlobject import *

database = "tests"

sqlhub.processConnection = connectionForURI('mysql://root:root@localhost/%s' % (database))

class users(SQLObject):
    user = StringCol()
    password = StringCol()
    nb_fichier = IntCol()

class noeud(SQLObject):
    id_sonde = StringCol()
    nb_files = IntCol()

class networks(SQLObject):
    id_network = StringCol
    network_king_id = StringCol()

class networks_status(SQLObject):
    id_network = StringCol()
    networks_status = StringCol()

def insert(kwargs, table):
    return table(**kwargs)

def select(kwargs, table):
    return table.selectBy(**kwargs)[0]

def update(forseach, kwargs, table):
        p = select(forseach, table)
        p.set(**kwargs)

def createTable():
    try :
        users.createTable()
    except:
        pass

    try :
        noeud.createTable()
    except:
        pass

    try :
        networks.createTable()
    except:
        pass

    try :
        networks_status.createTable()
    except:
        pass
createTable()

#print (__name__)
if __name__ == '__main__':

    log = "test"
    passwd = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
    samplename = {
 	   'user': log,
       'password': passwd
     }

    rep = select(samplename, users)
    x = rep
    print(x)
