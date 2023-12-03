from typing import List, Optional, Tuple


class Passphrase:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [line.strip().split(" ") for line in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.stringList = self.getInput()

    def getValid(self, isPart2: Optional[bool] = False) -> int:
        count = 0
        for strings in self.stringList:
            wordDict = set()
            for word in strings:
                key = self.generateKey(word) if isPart2 else word
                if key in wordDict:
                    break
                wordDict.add(key)
            else:
                count += 1
        return count

    def generateKey(self, word: str) -> Tuple[str]:
        charList = [0] * 26
        for char in word:
            charList[ord(char) - ord("a")] += 1
        return tuple(charList)


if __name__ == "__main__":
    passphrase = Passphrase()
    print("Day 4 part 1:", passphrase.getValid())
    print("Day 4 part 2:", passphrase.getValid(True))
