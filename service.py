import communication
import signal
import sys
import os

cmd = sys.argv[1]
print(cmd)
if cmd == "start":
	pid = os.fork()
	if (pid == 0):
		communication.Serveur()

if cmd == "stop":
	try:
		clt = communication.Client(1337)
		servpid = clt.askpid()
		os.killpg(servpid, signal.SIGTERM)
	except:
		print("Serveur isn't connected")
