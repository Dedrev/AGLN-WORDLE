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
        y+=1


    return y

    

class WordleCli():
    def __init__(self):
        self.database = DatabaseHandling.Database()


    def exit_curses(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        exit()


    def drawLeaderBoard(self):
        """
        Draws LEADERBOARD
        """
        self.stdscr.addstr(0,0, "LEADERBOARD", curses.color_pair(1))
        self.stdscr.addstr(1, 3, "Name", curses.color_pair(1))
        self.stdscr.addstr(1, 26, "Score", curses.color_pair(1))
        self.stdscr.addstr(1, 33, "Last Word", curses.color_pair(1))
        for i, leader in enumerate(self.database.getLeaderboard(nLeaders=self.player.leaderboard_len)):
            self.stdscr.addstr(i+2,0, str(i+1))
            self.stdscr.addstr(i+2, 3, leader[0])
            self.stdscr.addstr(i+2, 26, str(leader[2]))
            self.stdscr.addstr(i+2, 33, leader[1])

        self.stdscr.addstr(self.player.leaderboard_len * 2 + 1, 0, "Your HighScore: " + str(self.player.score))

    def failedScreen(self):
        self.createMenue(
            title="YOU LOST",
            options={
            "restart": self.startGame,
            "options": self.options,
            "quit": self.exit_curses
            },
            extraAction=self.drawLeaderBoard
        )

    def endScreen(self):
        self.createMenue(
            title="CONGRATS",
            options={
                "restart": self.startGame,
                "options": self.options,
                "quit": self.exit_curses
                }, 
                extraAction=self.drawLeaderBoard
                )

    def startGame(self):
        # Resets console
        self.stdscr.clear()
        # enables normal writing
        curses.nocbreak()
        # enables displaying of characters
        curses.echo()
        
        # init player and asks for user name in prompt
        self.stdscr.addstr(0,0,"Please Enter your Name")
        self.stdscr.move(1,0)
        # loops as long the name is empty
        while self.player.name == "":
            self.player.name = self.stdscr.getstr().decode("utf-8")
            if len(self.player.name) > 20:
                self.player.name = ""
                self.stdscr.addstr(2,0,"Name can have max 20 letters", curses.color_pair(2))
            self.stdscr.move(1,0)
            # clears line
            self.stdscr.clrtoeol()

        self.stdscr.clear()
        self.stdscr.refresh()
        # TODO: FOR SHOWCASING
        # self.player.level=50
        # Main Game Loop
        while (True):
            line = 0
            word = self.database.getRandWordByLength(self.player.level, table_name=self.player.lang)
            # If max length of words is reached endScreen is called or if activated endless mode is activated.
            if word == None:
                if self.player.endless_mode:
                    self.player.level = Player.level
                    word = self.database.getRandWordByLength(self.player.level, table_name=self.player.lang)
                else:
                    self.endScreen()    
            # TODO: FOR SHOWCASING
            # self.stdscr.addstr(20, 0, word)
            # UI Setup
            drawTitle(stdscr=self.stdscr, text="WORDLE", y=0)
            height, width = self.stdscr.getmaxyx()
            underside = height//4
            # creates white space for placing guessWords
            for i in range(underside):
                self.stdscr.addstr(height-i-2,0, " "*width, curses.color_pair(1))
    
            # Game Info
            self.stdscr.addstr(0,0,"Score: "+str(self.player.score), curses.color_pair(3))
            self.stdscr.addstr(1,0,"Level: "+str(self.player.level), curses.color_pair(1))
            self.stdscr.addstr(3,0,"Name: "+self.player.name, curses.color_pair(1))
            # level iterator
            while (True):

                # Move player to typing position
                self.stdscr.move(height-1, 0)
                guessWord = ""
                # checks if the word has the right amount of letters and checks, if the setting is set to true, if the word is in the db
                # else it loops again
                while (len(guessWord) != self.player.level 
                       and not (self.database.checkForEntry(guessWord, self.player.lang) if self.player.word_check else False)):
                    
                    guessWord = self.stdscr.getstr().decode("utf-8").upper()
                    self.stdscr.clrtoeol()

                colMapping = checkWord(guessWord=guessWord[:self.player.level], word=word)
                # Maps ansii color codes to curses format
                for i, mapping in enumerate(colMapping):
                    if mapping == Colors.GREEN:
                        self.stdscr.addstr(height-underside+line,i, guessWord[i], curses.color_pair(4))
                    elif mapping == Colors.YELLOW:
                        self.stdscr.addstr(height-underside+line,i, guessWord[i], curses.color_pair(5))
                    elif mapping == Colors.RED:
                        self.stdscr.addstr(height-underside+line,i, guessWord[i], curses.color_pair(6))
                line+=1
                # checkes if the word was right and levels up the player
                if guessWord.upper() == word.upper():
                    self.player.level += 1
                    self.player.allAttemps += Player.remainingAttempts - self.player.remainingAttempts
                    self.player.remainingAttempts = Player.remainingAttempts
                    self.player.lastGuessedWord = word
                    self.player.score += getScore(len(word), self.player.remainingAttempts)
                    self.stdscr.clear()
                    break

                # checks if player lost
                elif self.player.remainingAttempts <= 0:
                    # Writes Progress to Leaderboard
                    self.database.writeToLeaderboard(self.player.name, self.player.lastGuessedWord, str(self.player.score))
                    # Resets Player Data
                    self.player.remainingAttempts = Player.remainingAttempts
                    # Sends player to lose screen
                    self.failedScreen()

                self.player.remainingAttempts -= 1
                self.stdscr.refresh()


    # changes table lang to the other lang
    # TODO: Make it dynamicly so that new lists can be added.
    def changeLang(self):
        if self.player.lang == DatabaseHandling.GERMAN_TABLE:
            self.player.lang = DatabaseHandling.ENGLISH_TABLE
        elif self.player.lang == DatabaseHandling.ENGLISH_TABLE:
            self.player.lang = DatabaseHandling.GERMAN_TABLE
    
        self.options()

    def changeWordCheck(self):
        self.player.word_check = not self.player.word_check
        self.options()

    def changeEndlessMode(self):
        self.player.endless_mode = not self.player.endless_mode
        self.options()
 
    def options(self):
        self.createMenue(
            title="OPTIONS",
            options={
            "wordlist: " + self.player.lang: self.changeLang,
            "word check: " + str(self.player.word_check): self.changeWordCheck,
            "endless_mode: " + str(self.player.endless_mode): self.changeEndlessMode,
            "main menue": self.mainMenue
        })


    def createMenue(self, title: str, options: dict, extraAction= lambda: None):
        curses.noecho()
        curses.cbreak()
        k = 0
        cursor_y = 0

        # Clear and refresh the screen for a blank canvas
        self.stdscr.clear()
        self.stdscr.refresh()

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
            # Keyboard input decision tree
            if k == curses.KEY_DOWN and cursor_y < len(options)-1:
                cursor_y = cursor_y + 1
            elif k == curses.KEY_UP and cursor_y > 0:
                cursor_y = cursor_y - 1
            # code for keyboard enter not numpad
            if k == 10:
                list(options.values())[cursor_y]()

            height, width = self.stdscr.getmaxyx()
            start_y = int((height // 5))
            # draws WORDLE titel
            drawTitle(stdscr=self.stdscr, text=title, y=start_y)
            self.stdscr.refresh()
            # draws menue options
            start_y = int((height // 3))
            # Dynamicly draw highlighting
            for i, text in enumerate(options.keys()):
                start_y = drawUTFTextCenter(stdscr=self.stdscr, text=text, y=start_y, color_pair=curses.color_pair(3 if cursor_y == i  else 1))+ 2
            ##########
            extraAction()
            self.stdscr.refresh()
            # Wait for keyboard press
            k = self.stdscr.getch()

    # The Main Menue
    def mainMenue(self):
        self.createMenue(
            title="WORDLE",
            options={
            "start": self.startGame, 
            "options": self.options,
            "quit": self.exit_curses
        },
        extraAction=self.drawLeaderBoard) 

    def run_init(self, stdscr):
        self.stdscr = stdscr
        self.mainMenue()
        
    def run(self, player: Player):
        self.player = player
        curses.wrapper(self.run_init)

if __name__ == "__main__":
    WordleCli().run(Player())
    
