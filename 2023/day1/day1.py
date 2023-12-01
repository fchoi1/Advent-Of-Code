from typing import List, Optional


class Trebuchet:
    def getInput(self) -> List[str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x for x in file1.readlines()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.list = self.getInput()
        self.numMap = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }

    def getTotal(self, isPart2: Optional[bool] = False) -> int:
        total = 0
        startNum = endNum = None
        for string in self.list:
            first = last = None
            for i in range(len(string)):
                if isPart2:
                    startNum = self.checkLetters(i, string)
                    endNum = self.checkLetters(i, string, True)

                if not first:
                    first = (
                        string[i]
                        if string[i].isdigit() and not startNum
                        else self.numMap.get(startNum, None)
                    )

                if not last:
                    last = (
                        string[-i - 1]
                        if string[-i - 1].isdigit() and not endNum
                        else self.numMap.get(endNum, None)
                    )

                if first and last:
                    break
            digit = first + last
            total += int(digit)
        return total

    def checkLetters(self, i: int, string: str, reverse: Optional[bool] = False) -> str:
        start, end, step = (i, i + 5, 1) if not reverse else (-i - 5, -i, -1)
        for _ in range(5, 2, -1):
            substring = string[start:end:step]
            if substring in self.numMap:
                return substring
        return None


if __name__ == "__main__":
    trebuchet = Trebuchet()
    print("Day 1 part 1:", trebuchet.getTotal())
    print("Day 1 part 2:", trebuchet.getTotal(True))
