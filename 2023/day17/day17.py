from typing import List, Optional, Tuple, Set


class Lava:
    def getInput(self) -> List[List[List[str]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(x.strip()) for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()

    def getTotal(self):
        total = 0
        return total


if __name__ == "__main__":
    lava = Lava()
    print("Day 16 part 1:", lava.getTotal())
