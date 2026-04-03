from main import Player
from DatabaseHandling import Database

class Engine:
    def __init__(self, player: Player):
        self.database = Database()
        self.player = player
    
    def run(self):
        raise Exception("Method is not Implemented")