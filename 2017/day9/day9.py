from typing import Optional


class Stream:
    def getInput(self) -> str:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return file1.readline().strip()

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.stream = self.getInput()
        self.score = self.garbage = 0
        self.calculateStream(0, 0)

    def calculateStream(self, index: int, level: int) -> None:
        garbage = False
        while index < len(self.stream):
            sym = self.stream[index]
            if not garbage:
                if sym == "<":
                    garbage = True
                elif sym == "{":
                    score, index = self.calculateStream(index + 1, level + 1)
                    self.score += score
                elif sym == "}":
                    return level, index
            else:
                self.garbage += 1
                if sym == ">":
                    garbage = False
                    self.garbage -= 1
                elif sym == "!":
                    self.garbage -= 1
                    index += 1
            index += 1

    def getScore(self) -> int:
        return self.score

    def getGarbage(self) -> int:
        return self.garbage


if __name__ == "__main__":
    stream = Stream()
    print("Day 9 part 1:", stream.getScore())
    print("Day 9 part 2:", stream.getGarbage())
