import sqlite3

GERMAN_TABLE = "german_word_list"
ENGLISH_TABLE = "english_word_list"

class Database:

    def __init__(self, file="wordle.db"):
        self.con = sqlite3.connect(file)

    def getLeaderboard(self, nLeaders=5) -> list[tuple[str, str, int]]:
        '''
        Holt eine bestimmte anzahl an leaders aus der highscore Tabelle
        '''
        cur = self.con.cursor()
        cur.execute("SELECT name, lastword, score FROM highscores ORDER BY score DESC")

        return cur.fetchmany(nLeaders)
    
    def getRandWordByLength(self, l=3, table_name=GERMAN_TABLE) -> str | None:
        '''
        Holt ein Random wort aus der angegebenen Tabelle
        mit einer angegebenen Leange
        '''
        cur = self.con.cursor()
        cur.execute(f"SELECT word FROM {table_name} WHERE LENGTH(word) = ? ORDER BY RANDOM() LIMIT 1",
                    (l,))

        result = cur.fetchone()
        if result == None:
            return result
        return result[0]
      
    def writeToLeaderboard(self, name: str, lastword: str, score: str):
        '''
        Schreibt einen eintrag in die highscore Tabelle 
        '''
        cur = self.con.cursor()
        cur.execute("INSERT INTO highscores (name, lastword, score) VALUES (?,?,?)",
                    (name, lastword, score))
        self.con.commit()
        cur.close()

    def checkForEntry(self, word, table_name=GERMAN_TABLE):
        if word == "":
            return False
        cur = self.con.cursor()
        cur.execute(f"SELECT 1 FROM {table_name} WHERE word = ?", (word,))
        return cur.fetchone() != None

if __name__ == "__main__":
    db = Database()

    print(db.getRandWordByLength(l=3, table_name=GERMAN_TABLE))
    print(db.writeToLeaderboard(name="Markus", lastword="LASTWORD", score=str(1024024202)))
    print(db.getLeaderboard(nLeaders=3))
