from typing import List, Optional, Tuple


class Expansion:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(s.strip()) for s in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()
        self.width = len(self.map[0])
        self.rows, self.cols = self.getExpanded()
        self.gals = self.getGalaxies()

    def getExpanded(self) -> Tuple[List[int]]:
        rows = [i for i, row in enumerate(self.map) if all(x == "." for x in row)]
        cols = [i for i in range(self.width) if all(row[i] == "." for row in self.map)]
        return rows, cols

    def getGalaxies(self) -> List[Tuple[int]]:
        return [
            (i, j)
            for i, row in enumerate(self.map)
            for j, char in enumerate(row)
            if char == "#"
        ]

    def getDist(self, pos1: Tuple[int], pos2: Tuple[int], isPart2: bool) -> int:
        inc = 1
        if isPart2:
            inc = 10 - 1 if self.useTest else 1_000_000 - 1
        d = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        for row in self.rows:
            if min(pos1[0], pos2[0]) < row < max(pos1[0], pos2[0]):
                d += inc
        for col in self.cols:
            if min(pos1[1], pos2[1]) < col < max(pos1[1], pos2[1]):
                d += inc
        return d

    def getTotal(self, isPart2: Optional[bool] = False) -> int:
        total = 0
        for i, first in enumerate(self.gals):
            for second in self.gals[i + 1 :]:
                total += self.getDist(first, second, isPart2)
        return total


if __name__ == "__main__":
    expansion = Expansion()
    print("Day 11 part 1:", expansion.getTotal())
    print("Day 11 part 2:", expansion.getTotal(True))
