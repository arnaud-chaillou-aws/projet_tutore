class generator(object):
    """
    This class is a ID generator for our em2a network
    """
    @staticmethod
    def getRandomCode():
        from uuid import uuid4
        return str(uuid4().hex)

    @staticmethod
    def getPassword(password=None):
        from hashlib import md5
        if password is None:
            from ssl import RAND_bytes
            return md5(RAND_bytes(16)).hexdigest()
        else:
            return md5(password.encode()).hexdigest()
