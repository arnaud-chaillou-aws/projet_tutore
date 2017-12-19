import socket
import base64
import sys
import rsa
import crypto

def sender(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 1337))
    packet = data
    taille = base64.b64encode(str(len(packet)).encode("utf-8"))
    s.send(taille + b'\n')
    s.send(data)
    print(len(data))
    s.close()

if __name__ == "__main__":
    f = open(sys.argv[1],"rb")
    data = f.read()
    print(len(data))
    sender(data)
