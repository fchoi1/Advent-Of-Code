from typing import Optional, List, Dict


class Lobby:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x.strip() for x in file1.readlines()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.lines = self.getInput()
        print(self.lines)

    def getTiles(self) -> int:
        pass


if __name__ == "__main__":
    lobby = Lobby()
    print("Day 24 part 1:", lobby.getTiles())
    print("Day 24 part 2:")
