import sqlite3

# TODO Make it more user friendly.
# TODO Make it so that users can pass a wordlistfile to use.
def setup():
    con = sqlite3.connect("wordle.db")


    cur = con.cursor()

    cur.execute("""
                CREATE TABLE highscores(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, 
                    lastword TEXT, 
                    score NULL,
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )""")
    cur.execute("""
                CREATE TABLE english_word_list(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    word TEXT NOT NULL
                )""")
    cur.execute("""
                CREATE TABLE german_word_list(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    word TEXT NOT NULL
                )""")

    print("Created Tables")
    print("Populating Tables with data")
    
    with open("wordlist-german.txt", "r") as f:
        while True:
            word = f.readline().rstrip()
            if word == '':
                break
            cur.execute("""
                    INSERT INTO german_word_list (word) VALUES
                        (?)
                    """,
                    (word,))
            
    with open("wordlist-english.txt", "r") as f:
        while True:
            word = f.readline().rstrip()
            if word == '':
                break
            cur.execute("""
                    INSERT INTO english_word_list (word) VALUES
                        (?)
                    """,
                    (word,))

    con.commit()
        
if __name__ == "__main__":
    setup()