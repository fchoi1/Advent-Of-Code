def getInput():
    file1 = open('input.txt', 'r')
    # file1 = open('input-test.txt', 'r')
    Lines = file1.readlines()
    data = []
    # Get input data
    for line in Lines:
        data.append(line.strip())
    return data

def main():
    """ Main entry point of the app """
    inputData = getInput()

    for line in inputData:
        print('day 6 part 1:', getStartofPacket(line))
        print('day 6 part 2:', getStartofPacket(line,14)) 
        

      
def getStartofPacket(word: str, length: int = 4):
    letters = []
    for i, char in enumerate(word):
        letters.append(char)
        if len(letters) >= length:
            if isUnique(letters) and len(letters):
                return i + 1
            else:
                letters.pop(0)
    return None
        
def isUnique(word: list[str]):
    letters = [*range(1,26)]
    for char in word:
        charNum = ord(char) - ord('a')
        if charNum in letters:
            letters.pop(letters.index(charNum))
        else:
            return False
    return True
    


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()