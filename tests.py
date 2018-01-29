import mysqlcmd
class initialisateur:
    def getchain(self):
        output = []
        selector = {'forselector': 0}
        chain = mysqlcmd.selectall(selector, mysqlcmd.Hash)
        chain = chain.orderBy('numero')
        if chain.count == 0:
            return output
        for x in range (chain.count()):
            if chain[x].numero == x:
                output.append(chain[x].val_hash)
        return output

    def getnode(self, id):
        output = []
        selector = {'network': id}
        chain = mysqlcmd.selectall(selector, mysqlcmd.noeud)
        chain = chain.orderBy('id')
        if chain.count() == 0:
            raise SystemError("Il n'y a aucun noeud dans ce réseau")
        for x in range (0, chain.count(), 1):
            print(x, chain.count())
            if chain[x].id == x+1:
                if test(chain[x].sonde_ip) = True:
                    output.append(chain[x].sonde_ip)
        return output

x=initialisateur()
print(x.getnode("MTUxNzIzNTI5OC4xOTI4MDcy1GzOA5nW/nFh3/aKrETrmmlj/S+KRKNF8BwNSABzcm0="))
