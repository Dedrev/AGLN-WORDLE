import sys,os
import curses
from curses.textpad import Textbox
import pyfiglet
import atexit
from main import Player
import DatabaseHandling
from HelperFunctions import *

def drawUTFTextCenter(stdscr, text, y, color_pair):
    """
    Draws Centered Title with highlighting and background.
    """
    text = pyfiglet.figlet_format(text)
    lines = text.split("\n")
    height, width = stdscr.getmaxyx()
    maxLength = max([len(l) for l in lines])
    x = int((width // 2) - (maxLength // 2))

    # Iterates over string except for the last line reason: Symmetry
    for line in lines[:-1]:
        stdscr.addstr(y, x, line, color_pair)
        y += 1

    return y

def drawTitle(stdscr, text, y):
    """
    Draws Centered Title without highlighting.
    """
    text = pyfiglet.figlet_format(text)
    lines = text.split("\n")
    height, width = stdscr.getmaxyx()
    maxLength = max([len(l) for l in lines])
    x = int((width // 2) - (maxLength // 2))
    
    for line in lines[:-1]:
        stdscr.addstr(y, x, line)


    return y

class WordleCli():
    def __init__(self):
        self.database = DatabaseHandling.Database()

    def drawLeaderBoard(self, stdscr):
        """
        Draws LEADERBOARD
        """
        stdscr.addstr(0,0, "LEADERBOARD", curses.color_pair(1))
        stdscr.addstr(1, 3, "Name", curses.color_pair(1))
        stdscr.addstr(1, 26, "Score", curses.color_pair(1))
        stdscr.addstr(1, 33, "Last Word", curses.color_pair(1))
        for i, leader in enumerate(self.database.getLeaderboard()):
            stdscr.addstr(i+2,0, str(i+1))
            stdscr.addstr(i+2, 3, leader[0])
            stdscr.addstr(i+2, 26, str(leader[2]))
            stdscr.addstr(i+2, 33, leader[1])

    def failedScreen(self, stdscr):
        # Locks controlls for Menue
        curses.cbreak()
        curses.noecho()
        stdscr.clear()
        stdscr.refresh()

        self.drawLeaderBoard(stdscr)

        k = 0
        cursor_y = 0
        while (True):
            # Decision tree
            if k == curses.KEY_DOWN and cursor_y < 1:
                cursor_y = cursor_y + 1
            elif k == curses.KEY_UP and cursor_y > 0:
                cursor_y = cursor_y - 1
            # code for keyboard enter not numpad
            elif k == 10:
                if cursor_y == 0:
                    return
                elif cursor_y == 1:
                    exit()

            height, width = stdscr.getmaxyx()
            # UI
            start_y = int((height // 5))
            drawTitle(stdscr=stdscr, text="WORDLE", y=start_y)

            start_y = int((height // 3))
            # Dynamicly draw highlighting
            start_y = drawUTFTextCenter(stdscr=stdscr, text="restart", y=start_y, color_pair=curses.color_pair(3 if cursor_y == 0  else 1))+ 2
            start_y = drawUTFTextCenter(stdscr=stdscr, text="quit", y=start_y, color_pair=curses.color_pair(3 if cursor_y == 1  else 1))
            ###############
            
            curses.use_default_colors()
            stdscr.refresh()
            k = stdscr.getch()

    def startGame(self, stdscr):
        # Resets console
        stdscr.clear()
        # enables normal writing
        curses.nocbreak()
        # enables displaying of characters
        curses.echo()
        
        # init player and asks for user name in prompt
        stdscr.addstr(0,0,"Please Enter your Name")
        stdscr.move(1,0)
        # loops as long the name is empty
        while self.player.name == "":
            self.player.name = stdscr.getstr().decode("utf-8")
            if len(self.player.name) > 20:
                self.player.name = ""
                stdscr.addstr(2,0,"Name can have max 20 letters", curses.color_pair(2))
            stdscr.move(1,0)
            # clears line
            stdscr.clrtoeol()

        stdscr.clear()
        stdscr.refresh()
        # Main Loop
        # Loops  
        while (True):
            line = 0
            word = self.database.getRandWordByLength(self.player.level, table_name=self.player.lang)
            # UI Setup
            drawTitle(stdscr=stdscr, text="WORDLE", y=0)
            height, width = stdscr.getmaxyx()
            underside = height//4
            # creates white space for placing guessWords
            for i in range(underside):
                stdscr.addstr(height-i-2,0, " "*width, curses.color_pair(1))
    
            # Game Info
            stdscr.addstr(0,0,"Score: "+str(self.player.score), curses.color_pair(3))
            stdscr.addstr(1,0,"Level: "+str(self.player.level), curses.color_pair(1))
            stdscr.addstr(3,0,"Name: "+self.player.name, curses.color_pair(1))
            # level iterator
            while (True):

                # Move player to typing position
                stdscr.move(height-1, 0)
                guessWord = ""
                while (len(guessWord) !=self.player.level):
                    guessWord = stdscr.getstr().decode("utf-8").upper()
                    stdscr.clrtoeol()
                colMapping = checkWord(guessWord=guessWord[:self.player.level], word=word)
                # Maps ansii color codes to curses format
                for i, mapping in enumerate(colMapping):
                    if mapping == Colors.GREEN:
                        stdscr.addstr(height-underside+line,i, guessWord[i], curses.color_pair(4))
                    elif mapping == Colors.YELLOW:
                        stdscr.addstr(height-underside+line,i, guessWord[i], curses.color_pair(5))
                    elif mapping == Colors.RED:
                        stdscr.addstr(height-underside+line,i, guessWord[i], curses.color_pair(6))
                line+=1
                # checkes if the word was right    
                if guessWord == word:
                    self.player.level += 1
                    self.player.allAttemps += Player.remainingAttempts - self.player.remainingAttempts
                    self.player.remainingAttempts = Player.remainingAttempts
                    self.player.lastGuessedWord = word
                    self.player.score = getScore(len(word), self.player.remainingAttempts)
                    stdscr.clear()
                    break
                # checks if player lose
                elif self.player.remainingAttempts <= 0:
                    self.database.writeToLeaderboard(self.player.name, self.player.lastGuessedWord, str(self.player.score))
                    self.player.remainingAttempts = Player.remainingAttempts
                    # Sends player to lose screen
                    self.failedScreen(stdscr=stdscr)

                    # Releases the controlls for the player
                    curses.nocbreak()
                    curses.echo()
                    # Resets player and Game
                    self.player = Player()
                    break

                self.player.remainingAttempts -= 1
                stdscr.refresh()

    def options(self, stdscr):
        curses.noecho()
        k = 0
        cursor_y = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Sets background to standard color
        curses.use_default_colors()

        # Main Menue Loop
        while (True):
            # Keyboard input decision tree
            if k == curses.KEY_DOWN and cursor_y < 1:
                cursor_y = cursor_y + 1
            elif k == curses.KEY_UP and cursor_y > 0:
                cursor_y = cursor_y - 1
            # code for keyboard enter not numpad
            elif k == 10:
                stdscr.clear()
                stdscr.refresh()
                
                # When on start
                if cursor_y == 0:
                    if self.player.lang == DatabaseHandling.GERMAN_TABLE:
                        self.player.lang = DatabaseHandling.ENGLISH_TABLE
                    elif self.player.lang == DatabaseHandling.ENGLISH_TABLE:
                        self.player.lang = DatabaseHandling.GERMAN_TABLE
                # When on quit
                elif cursor_y == 1:
                    return;

            height, width = stdscr.getmaxyx()
            start_y = int((height // 5))
            # draws WORDLE titel
            drawTitle(stdscr=stdscr, text="OPTIONS", y=start_y)
            # draws menue options
            start_y = int((height // 3))
            # Dynamicly draw highlighting
            start_y = drawUTFTextCenter(stdscr=stdscr, text="wordlist: " + self.player.lang, y=start_y, color_pair=curses.color_pair(3 if cursor_y == 0  else 1))+ 2
            start_y = drawUTFTextCenter(stdscr=stdscr, text="main menue", y=start_y, color_pair=curses.color_pair(3 if cursor_y == 1  else 1))
            ##########
            stdscr.refresh()
            # Wait for keyboard press
            k = stdscr.getch()








    def draw_menu(self, stdscr):
        curses.noecho()
        k = 0
        cursor_y = 0

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Sets color prefaps
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

        # Sets background to standard color
        curses.use_default_colors()

        # Main Menue Loop
        while (True):
            self.drawLeaderBoard(stdscr)

            # Keyboard input decision tree
            if k == curses.KEY_DOWN and cursor_y < 2:
                cursor_y = cursor_y + 1
            elif k == curses.KEY_UP and cursor_y > 0:
                cursor_y = cursor_y - 1
            # code for keyboard enter not numpad
            elif k == 10:
                # When on start
                if cursor_y == 0:
                    self.startGame(stdscr)
                # When on options  
                if cursor_y == 1:
                    self.options(stdscr)
                # When on quit
                elif cursor_y == 1:
                    exit()
                    
            self.drawLeaderBoard(stdscr)

            height, width = stdscr.getmaxyx()
            start_y = int((height // 5))
            # draws WORDLE titel
            drawTitle(stdscr=stdscr, text="WORDLE", y=start_y)
            # draws menue options
            start_y = int((height // 3))
            # Dynamicly draw highlighting
            start_y = drawUTFTextCenter(stdscr=stdscr, text="start", y=start_y, color_pair=curses.color_pair(3 if cursor_y == 0  else 1))+ 2
            start_y = drawUTFTextCenter(stdscr=stdscr, text="options", y=start_y, color_pair=curses.color_pair(3 if cursor_y == 1 else 1))+ 2
            start_y = drawUTFTextCenter(stdscr=stdscr, text="quit", y=start_y, color_pair=curses.color_pair(3 if cursor_y == 2  else 1))
            ##########
            stdscr.refresh()
            # Wait for keyboard press
            k = stdscr.getch()

    def run(self, player: Player):
        self.player = player
        curses.wrapper(self.draw_menu)

if __name__ == "__main__":
    WordleCli().run(Player())
    
