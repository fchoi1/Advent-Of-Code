from typing import List, Optional


class Blizzard:
    def getInput(self) -> List[str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                data.append(list(line.strip()))
            return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()


if __name__ == "__main__":
    blizzard = Blizzard(False)
    print("Day 25 part 1:")
    print("Day 25 part 2:")
