
def getScore(wordLentgh,attempts) -> int:
    '''
    Gibt den Score für das aktuelle Level raus
    '''
    return wordLentgh * 10 + ((5 - attempts) *5)

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
    if(word[position] == letter):
        return True
    return False

def getWordGuess() -> dict:
    '''
    Gibt die Buchstaben und ihre Position zurück
    '''
    word = input()
    word = word.upper()
    result = {}
    for i in range(len(word)):
        result[i] = word[i]
    return result