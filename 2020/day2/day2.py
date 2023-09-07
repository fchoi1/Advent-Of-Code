from typing import List, Optional
import re


class Password:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
            passwords, letters = [], []
            delimiters = "|".join(map(re.escape, ["-", " ", ": "]))
            for line in Lines:
                splited = re.split(delimiters, line.strip())
                passwords.append(splited[3])
                letters.append([int(splited[0]), int(splited[1]), splited[2]])
        return (letters, passwords)

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.letters, self.passwords = self.getInput()

    def checkOccurence(self) -> int:
        count = 0
        for letter, password in zip(self.letters, self.passwords):
            if self.isValidPassword(password, letter):
                count += 1
        return count

    def isValidPassword(self, password: str, letter: List[int | str]) -> bool:
        minNum, maxNum = letter[:2]
        char = letter[2]
        return minNum <= password.count(char) <= maxNum

    def isValidPassword2(self, password: str, letter: List[int | str]) -> bool:
        one, two = letter[:2]
        char = letter[2]
        return (password[one - 1] == char) ^ (password[two - 1] == char)

    def checkSubstring(self) -> int:
        count = 0
        for letter, password in zip(self.letters, self.passwords):
            if self.isValidPassword2(password, letter):
                count += 1
        return count


if __name__ == "__main__":
    password = Password()
    print("Day 2 part 1:", password.checkOccurence())
    print("Day 2 part 2:", password.checkSubstring())
