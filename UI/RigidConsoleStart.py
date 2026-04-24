from UI.RigidConsole import *


def start():
    startMenue = Window("Test")

    Text(text="Test")

    startMenue.addProperty(Text)

    windows = [startMenue]


    slideEngine = SlideEngine(windows)

    slideEngine.setup()
    slideEngine.start()