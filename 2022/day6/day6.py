from typing import List, Optional


def getInput(useTest) -> List[str]:
    inputFile = "input-test.txt" if useTest else "input.txt"
    with open(inputFile, "r") as file1:
        return [x.strip() for x in file1]


def main(useTest: Optional[bool] = False) -> None:
    inputData = getInput(useTest)

    for line in inputData:
        print("day 6 part 1:", getStartofPacket(line))
        print("day 6 part 2:", getStartofPacket(line, 14))


def getStartofPacket(word: str, length: int = 4) -> int:
    letters = []
    for i, char in enumerate(word):
        letters.append(char)
        if len(letters) >= length:
            if isUnique(letters) and len(letters):
                return i + 1
            else:
                letters.pop(0)
    return 0


def isUnique(word: List[str]) -> bool:
    letters = [*range(1, 26)]
    for char in word:
        charNum = ord(char) - ord("a")
        if charNum in letters:
            letters.pop(letters.index(charNum))
        else:
            return False
    return True


if __name__ == "__main__":
    main()
