"""
Blockchain support for the em2a node network.
"""

from config import CONFIG

class Blockchain(object):
    def __init__(self, CONFIG):
        self.config = CONFIG
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
