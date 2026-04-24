import UI.BaseClass as Base
import os
import pyfiglet
import time
from pynput import keyboard
import curses


class Window(Base.Window):
    name = ""
    properties = []
    def __init__(self, player, name="TheGreatestWindowThatHasEverLived"):
        super().__init__(player)
        self.name = name

    def addProperty(self, property: Property):
        self.properties.append(property)

    # TODO Implement position size etc.
    def render(self):
        canvas = "\n"*os.get_terminal_size().lines
        for property in self.properties:
            property().curPos()
            canvas += property().draw()



class Property:
    curPos: list[float,float]

    def __init__(self, curPos=[0,0]):
        self.curPos = curPos

    def callback():
        pass

    def draw(self):
        raise Exception("Not implemented yet")
    
    def onKeyPress(self, key: str, engine: Base.Engine):
        pass


class Rectangle(Property):
    colorCode = "\x1b[47m"
    colorReset = "\x1b[0m"
    size = [0, 0] # Relative size of rectangle

    def __init__(self, curPos=[0,0], size = [0,0]):
        super().__init__(curPos)

    def draw(self) -> list[
        str, # Data to Write
        list[int, int] # Relative cursor position after Write
        ]:
        rect = self.colorCode
        for i in range(self.size[1]):
            rect += " "*self.size[0]
            rect += "\x1b[B" # Move cur down
            rect += f"\x1b[{self.curPos[0]}G" # Move cur left n times
        return rect + self.colorReset, self.size

class Background(Rectangle):
    def __init__(self):
        tSize = os.get_terminal_size()
        super().__init__([0,0], [tSize.columns, tSize.lines])

class Text(Property):
    text=""

    def __init__(self, curPos=[0, 0], text=""):
        super().__init__(curPos)

    def draw(self):
        text = pyfiglet.figlet_format("WORDLE")
        # curPos[0] must be bigger than 0
        print(text, end="")

class Button(Property):

    properties = []

    def __init__(self, curPos=[0, 0], size=[1,1], text=""):
        super().__init__(curPos)
        self.rectangle = Rectangle(curPos=curPos, size=size)
        self.text = Text(curPos=curPos)
        self.properties = [
            Rectangle(curPos=curPos, size=size),
            Text(curPos=curPos, text=text)
        ]

    def event(self):
        raise Exception("Not implemented")

    def draw(self):
        for property in self.properties:
            property.draw()
        
class Menue(Property):
    options = [
    ]

    selected = 0

    def __init__(self, curPos=[0,0], buttonOptionList: list[Button] = []):
        super().__init__(curPos=curPos)
        self.options = buttonOptionList

    def onKeyPress(self, key: str, engine: Base.Engine):
        if key in ["up", "w"]:
            selected += -1 if self.selected > 0 else 0
        elif key in ["down", "s"]:
            selected += -1 if self.selected < len(self.options) else 0
        elif key == "enter":
            self.options[self.selected].event()
        
    def draw(self):
        for option in self.options:
            option().draw()


class SlideEngine(Base.Engine):
    def __init__(self, windows: list[Window]):
        super().__init__(windows)
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

    def start(self):
        listener = keyboard.Listener(
            on_press=self.inputHandler
        )
        listener.start()
        while (True):
            time.sleep(0.2)

    def inputHandler(self, key):
        for property in self.windows[self.selectedWindow].properties:
            property().onKeyPress(key=key, engine=self)
        self.update()
    
    def update(self):
        self.windows[self.selectedWindow].render()

    def exit(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()