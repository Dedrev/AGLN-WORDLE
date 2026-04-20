from UI.BaseClass import Engine
from HelperFunctions import *
from main import Player
import DatabaseHandling

# NOTE Maybe add a difficulty system with limiting attempts or something like that.
# NOTE THIS IS AN EXAMPLE

class Console(Engine):
    def __init__(self, player: Player):
        super().__init__(player=player)

    # startpunkt
    def run(self):
        self.showDashboard()
        self.setupPrompt()
        while True:
            languageInput = input("Möchten sie das Spiel in Englisch oder Deutsch Spielen? (D/E): ")
            if(languageInput.lower() == "e"):
                print("Playing in English")
                table = DatabaseHandling.ENGLISH_TABLE
            elif(languageInput.lower() == "d"):
                print("Playing in German")
                table = DatabaseHandling.GERMAN_TABLE
            else:
                print("Invalid Input. Please try again.")
                continue
            self.startGame(table)
            if input("Do you want to Retry. (Y/n)").lower() == "n":
                print("Leaving Game")
                break

    def showDashboard(self):
        print("WELCOME TO WORDLE")
        print("LEADERBOARD")
        for i in self.database.getLeaderboard():
            print(f"Name: {i[0]}, Last Word: {i[1]}, Score: {i[2]}")

    
    def setupPrompt(self):
        self.player.name = input("Please Enter your Username: ")

    def startGame(self, table):
        while True:
            # TODO Add handling for when level is higher than highest word
            word = self.database.getRandWordByLength(self.player.level, table_name=table)
            print(f"Starting with Level {self.player.level}")
            while True:
                guessWord = input("Guess: ")[:self.player.level]
                if len(guessWord) != self.player.level:
                    print(f"Please enter a word with {self.player.level} letters.")
                    continue
                colMapping = checkWord(guessWord=guessWord, word=word)
                print(applyMarkerTokWord(guessWord,colMapping), Colors.END)
                print(f"Remaining Attempts: {self.player.remainingAttempts}")
                if guessWord.upper() == word.upper():
                    print("The word was guessed right.")
                    print("Going to the next level")
                    self.player.level += 1
                    self.player.allAttemps += Player.remainingAttempts - self.player.remainingAttempts
                    self.player.remainingAttempts = Player.remainingAttempts
                    self.player.score += getScore(len(word), self.player.remainingAttempts)
                    self.player.lastGuessedWord = word
                    break
                elif self.player.remainingAttempts <= 0:
                    print("To many attempts. Failed to Guess word." \
                    "The word was: ", word)
                    print("Saving progress to Leaderboard")
                    self.database.writeToLeaderboard(self.player.name, self.player.lastGuessedWord, self.player.score)
                    self.player.remainingAttempts = Player.remainingAttempts
                    return
                self.player.remainingAttempts -= 1
