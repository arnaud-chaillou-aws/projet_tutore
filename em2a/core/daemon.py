import os
import sys
import signal
import resource

import server

from twisted.python import log
from setuplog import OBSERVER

log.addObserver(OBSERVER.emit)


class DeamonAlreadyOnlineError(Exception):
    def __init__(self):
        Exception.__init__(self)

def daemonize():
    # log.startLogging(open("/home/arnaud/projet_tutore/v2/em2a/log/daemon.log","a"))
    log.startLogging(sys.stdout)
    try:
        pidfile = open("/tmp/.em2apid","r")
        pid = int(pidfile.readline())
        if pid :
            raise DeamonAlreadyOnlineError()

    except FileNotFoundError:
        pass

    log.msg("AH")
    fatherpid = os.getpid()
    status = os.fork()

    if status > 0:
        sys.exit(0)

    # Set process as new session leader and process group leader
    log.msg("B")
    if status == 0:
        os.setsid()

        status = os.fork()

        if status > 0:
            sys.exit(0)

        log.msg("C")
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE);

        while soft > 2:
            try:
                os.close(soft)
            except:
                pass

            soft -= 1

        log.msg("D")
        fd = open("/tmp/test")
        os.dup2(fd.fileno(), 0)
        os.dup2(fd.fileno(), 1)
        os.umask(0)
        os.chdir('/')

        print("t")

        with open("/tmp/.em2apid", "w+") as pidfile:
            pid = os.getpid()
            pidfile.write(str(pid))

        with open("/tmp/testtestest", "a") as f:
            f.write("AH")
        # os.kill(fatherpid, signal.SIGUSR2)
        server.init()

if __name__ == '__main__':
    if sys.argv[1] == 'start':
        daemonize()

    elif sys.argv[1] == 'stop':
        try:
            with open("/tmp/.em2apid", "r") as f:
                pid = f.read()
                os.kill(int(pid),signal.SIGUSR2)
                os.remove("/tmp/.em2apid")

        except FileNotFoundError:
            print("service isn't started")
