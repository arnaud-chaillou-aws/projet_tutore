import mysqlcmd

def createtab(cred):
    tab = {
    'user': cred[0],
    'password': cred[1]
    }
    return tab

def authentification(cred):
    tab = createtab(cred)
    try :
        tmp = mysqlcmd.select(tab, mysqlcmd.users)
        return 0
    except:
        return 1

if __name__ == "__main__":
    authentification(("test","9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"))
