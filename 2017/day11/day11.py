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
        stepDir = {
            "n": (0, 1, 1),
            "s": (0, -1, -1),
            "ne": (1, 1, 0),
            "nw": (-1, 0, 1),
            "se": (1, 0, -1),
            "sw": (-1, -1, 0),
        }

        for step in self.steps:
            dx, dy, dz = stepDir[step]
            self.pos[0] += dx
            self.pos[1] += dy
            self.pos[2] += dz
            self.maxDist = max(self.maxDist, self.getDistance())


if __name__ == "__main__":
    hexGrid = HexGrid()
    print("Day 11 part 1:", hexGrid.getDistance())
    print("Day 11 part 2:", hexGrid.getMaxDistance())
