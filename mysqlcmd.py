from sqlobject import *

database = "tests"

sqlhub.processConnection = connectionForURI('mysql://root:root@localhost/%s' % (database))

class users(SQLObject):
    user = StringCol()
    password = StringCol()
    nb_fichier = IntCol()

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
        print("can't create users")
createTable()

#print (__name__)
# if __name__ == '__main__':
#     name = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
#     samplename = {
# 	   'name': name
#     }
#     """rep = select(samplename, fromclient)
#     x = rep.nb_capture
#     print(x)"""
