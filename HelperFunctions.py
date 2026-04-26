
class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    ORANGE = "\033[48:2:255:165:0m%s\033[m"

def getScore(wordLentgh: int,remainingAttempts: int) -> int:
    '''
    Gibt den Score für das aktuelle Level raus
    '''
    return wordLentgh * 10 + (remainingAttempts *5)

def checkForRightLetter(word: str,letter: str) -> bool:
    '''
    Überprüft ob der Buchstabe im Word vorhanden ist.
    '''
    if(letter.upper() in word.upper()):
        return True
    return False

def checkForRightPosition(word: str, letter: str, position: int) -> bool:
    '''
    Überprüf ob der Buchstabe an der richtigen Position steht
    '''
    if(word.upper()[position] == letter.upper()):
        return True
    return False

def checkWord(guessWord: str, word: str):
    '''
    Returns Color Mapping for a word.
    '''
    mapping = []
    for i, letter in enumerate(guessWord):
        rPos = checkForRightPosition(word=word, letter=letter, position=i)
        rLet = checkForRightLetter(word=word, letter=letter)
        if rPos:
            mapping.append(Colors.GREEN)
        elif rLet:
            mapping.append(Colors.YELLOW)
        else:
            mapping.append(Colors.RED)
    return mapping

def applyMarkerTokWord(word: str, colors: list[str]) -> str:
    '''
    Markiert per format [color, color, ......] den string mit der Angegeben farbe
    Dabei Repreasentiert jede farbe einen buchstaben.
    Die Farben sind in Colors hinterlegt.
    '''
    markedWord = ''
    for i, color in enumerate(colors):
        markedWord += color + word[i]
    return markedWord

if __name__ == "__main__":
    dummy = [Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.RED]
    print(applyMarkerTokWord("test", dummy))