from typing import List, Optional


class HexGrid:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x for x in file1.readline().strip().split(",")]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.steps = self.getInput()
        self.pos = [0, 0, 0]  # Q R P
        self.maxDist = 0
        self.runSteps()
        print(len(self.steps), self.pos)

    def getDistance(self) -> int:
        return sum(abs(x) for x in self.pos) // 2

    def getMaxDistance(self) -> int:
        return self.maxDist

    def runSteps(self) -> None:
        for step in self.steps:
            if step == "n":
                self.pos[1] += 1
                self.pos[2] += 1
            elif step == "s":
                self.pos[1] -= 1
                self.pos[2] -= 1
            elif step == "ne":
                self.pos[0] += 1
                self.pos[1] += 1
            elif step == "nw":
                self.pos[0] -= 1
                self.pos[2] += 1
            elif step == "se":
                self.pos[0] += 1
                self.pos[2] -= 1
            elif step == "sw":
                self.pos[0] -= 1
                self.pos[1] -= 1
            self.maxDist = max(self.maxDist, self.getDistance())


if __name__ == "__main__":
    hexGrid = HexGrid()
    print("Day 11 part 1:", hexGrid.getDistance())
    print("Day 10 part 2:", hexGrid.getMaxDistance())
