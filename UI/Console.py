from UI.BaseClass import Engine
from HelperFunctions import *
from main import Player
import DatabaseHandling

# NOTE Maybe add a difficulty system with limiting attempts or something like that.

class Console(Engine):
    def __init__(self, player: Player):
        super().__init__(player=player)

    def run(self):
        self.showDashboard()
        self.setupPrompt()
        while True:
            self.startGame()
            if input("Do you want to Retry. (Y/n)").lower() == "n":
                print("Leaving Game")
                break


    def showDashboard(self):
        print("WELCOME TO WORDLE")
        print("LEADERBOARD")
        for i in self.database.getLeaderboard():
            print(i[0], "    ", i[1],"    " ,  i[2])

    def setupPrompt(self):
        self.player.name = input("Please Enter your Username: ")

    def startGame(self):
        while True:
            # TODO Add handling for when level is higher than highest word
            language = input("Möchten sie das Spiel in Englisch oder Deutsch Spielen? (D/E): ")
            if(language.lower() == "e"):
                print("Playing in English")
                word = self.database.getRandWordByLength(self.player.level, table_name=DatabaseHandling.ENGLISH_TABLE)
            elif(language.lower() == "d"):
                print("Playing in German")
                word = self.database.getRandWordByLength(self.player.level, table_name=DatabaseHandling.GERMAN_TABLE)
            print(f"Starting with Level {self.player.level}")
            
            while True:
                guessWord = input("Guess: ")[:self.player.level]
                colMapping = checkWord(guessWord=guessWord, word=word)
                print(applyMarkerTokWord(guessWord,colMapping), Colors.END)
                if guessWord.upper() == word.upper():
                    print("The word was guessed right.")
                    print("Going to the next level")
                    self.player.level += 1
                    self.player.allAttemps += Player.remainingAttempts - self.player.remainingAttempts
                    self.player.remainingAttempts = Player.remainingAttempts
                    self.player.lastGuessedWord = word
                    getScore(len(word), self.player.remainingAttempts)
                    break
                elif self.player.remainingAttempts <= 0:
                    print("To many attempts. Failed to Guess word." \
                    "The word was: ", word)
                    print("Saving progress to Leaderboard")
                    self.database.writeToLeaderboard(self.player.name, self.player.lastGuessedWord, self.player.score)
                    self.player.remainingAttempts = Player.remainingAttempts
                    return
                self.player.remainingAttempts -= 1