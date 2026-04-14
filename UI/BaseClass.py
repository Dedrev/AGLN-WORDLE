from main import Player
from DatabaseHandling import Database
from os import get_terminal_size

class Window:
    def __init__(self, player: Player):
        self.database = Database()
        self.player = player
    
    def run(self):
        raise Exception("Method is not Implemented")
    
    def getSize(self):
        return get_terminal_size()
    
    def render(self):
        raise Exception("Not Implemented yet")
    
class Engine:
    def __init__(self):
        pass

    def setup():
        [print(i) for i in range(get_terminal_size().lines)]


    def start():
        raise Exception("Not implemented")