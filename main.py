if __name__ == "__main__":
    import HelperFunctions as hf
    import DatabaseHandling as db
    import setup

    print("hello world!")

    def databasePrompting() -> None:
        '''
        Wird aufgerufen wenn eine file nicht zugeanglich ist,
        oder wenn sie nicht existiert.
        Daraufhin wird ein dialog eroeffnet bei dem der User
        entscheiden kann ob eine db erstellen will oder den
        Prozess unterbrechen will.
        '''
        print("""Could not Database. 
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

    class Player:
        name : str
        score: int = 0
        level: int = 1
        levelAttemps: int = 0
        allAttemps: int = 0
    
    # Checks if the Database is active or not.
    try:
        open("wordle.db", "+w").close()
    except Exception as e:
        databasePrompting()

    player = Player

    hf.

else:
    raise Exception("This script cannot be importet")
