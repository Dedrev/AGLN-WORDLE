import UI.BaseClass as Base
import os
import pyfiglet


class SlideEngine(Base.Engine):
    windows = []
    def __init__(self):
        super().__init__()


class Window(Base.Window):
    properties = []
    def __init__(self):
        super().__init__(curPos=[0,0])

    def addProperty(self, property: Property):
        self.properties.append(property)

    # TODO Implement position size etc.
    def render(self):
        for i in self.properties:
            print(i, end="")

class Property:
    curPos: list[float,float]

    def __init__(self, curPos=[0,0]):
        self.curPos = curPos

    def draw(self):
        raise Exception("Not implemented yet")

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

class Title(Property):
    text=""

    def __init__(self):
        super().__init__()

    def draw(self):
        text = pyfiglet.figlet_format("WORDLE")
        # curPos[0] must be bigger than 0
        text.replace("\n", f"\033[B\033[{self.curPos[0]}G")