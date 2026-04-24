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
    windows = list[Window]
    selectedWindow = 0
    def __init__(self, windows = []):
        self.windows = windows

    def setup(self):
        [print() for i in range(get_terminal_size().lines)]

    def start():
        raise Exception("Not implemented")
    
    def inputHandler():
        raise Exception("Not implemented")
    
    def update():
        raise Exception("Not implemented")
    