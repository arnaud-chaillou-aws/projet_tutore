import socket
import threading
import base64
import rsa

def main():
    while (1):
        waiting()

def waiting():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 1337))
    s.listen(5)
    while True:
        (conn, (ip, port)) = s.accept()
        newthread = threading.Thread(target = reception, args=(ip, port, conn))
        newthread.start()

def reception(ip, port, conn):
    taille = b''
    buffer = b''
    i = ''
    while i != b'\n':
        i = conn.recv(1)
        taille += i
    taille = int(base64.b64decode(taille))
    while len(buffer) < taille:
        data = conn.recv(1024)
        buffer += data
    print(buffer)
    test = open("test","wb")
    test.write(buffer)

if __name__ == "__main__":
    main()
