import DatabaseHandling as db

class Player:
    name : str = ""
    score: int = 0
    level: int = 3
    remainingAttempts: int = 5
    allAttemps: int = 0
    lastGuessedWord: str = ""
    lang = db.GERMAN_TABLE 

if __name__ == "__main__":
    
    import HelperFunctions as hf
    import setup
    from UI.Console import Console    
    import UI.RigidConsoleStart as rgds
    import UI.RigidConsoleStart

    def databasePrompting() -> None:
        '''
        Wird aufgerufen wenn eine file nicht zugeanglich ist,
        oder wenn sie nicht existiert.
        Daraufhin wird ein dialog eroeffnet bei dem der User
        entscheiden kann ob eine db erstellen will oder den
        Prozess unterbrechen will.
        '''
        print("""Could not find Database. 
              It could be because of missing permissions
              or it could be because the Database was not created.""")
        print("Do you want to create the Database. (y/N)")
        createDatabase = input()
        if createDatabase == "y":
            setup.setup()
        elif createDatabase == "n" or createDatabase == "":
            print("Exiting Program")
            exit()
        else:
            print(f"""{createDatabase} is not a valid Argument.
                  Please try again. (y/N)""")
            databasePrompting()

    # Checks if the Database is active or not.
    try:
        open("wordle.db", "+r").close()
    except Exception as e:
        databasePrompting()

    while (True):
        player = Player()
        wordle_i = input("Worlde 1 or 2: ")
        if wordle_i == "1":
            console = Console(player)
            console.run()
        elif wordle_i == "2":
            UI.RigidConsoleStart.WordleCli().run(player)
