from typing import Optional, Dict, List


class GPU:
    def getInput(self) -> Dict[str, str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        enhance = {}
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                line = line.strip().split(" => ")
                enhance[line[0]] = line[1]
        return enhance

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.particles = self.getInput()
        self.grid = [".#.", "..#", "###"]
        self.size = 3
        print("init")

    def getPermutations(self):
        for
        pass

    def rotate(self, tile: List[List[str]]) -> str:
        return [list(row) for row in zip(*reversed(tile))]

    def generateKey(self, tile: List[List[str]]) -> str:
        key = "/".join("".join(row) for row in tile)
        return key

    def findMatch(self, rowStr: int) -> str:
        rows = [list(x) for x in rowStr.split("/")]
        for _ in range(4):
            rotated = self.rotate(rows)
            flipped = rotated[::-1]
            if self.generateKey(rotated) in self.particles:
                return self.particles[self.generateKey(rotated)]
            if self.generateKey(flipped) in self.particles:
                return self.particles[self.generateKey(flipped)]
            rows = rotated
        return ""

    def updateGrid(self, grid: List[List[str]], size: int):
        self.grid = []
        for row in grid:
            for i in range(size + 1):
                rowStr = [string.split("/")[i] for string in row]
                rowStr = "".join(rowStr)
                self.grid.append(rowStr)

    def increaseGrid(self, grid: List[List[str]]) -> List[List[str]]:
        return [[self.findMatch(string) for string in row] for row in grid]

    def getKeys(self, size: int):
        pGrid = []
        for j in range(0, len(self.grid), size):
            pRows = []
            for i in range(0, len(self.grid), size):
                key = self.grid[j][i : i + size]
                for n in range(1, size):
                    key += "/" + self.grid[j + n][i : i + size]
                pRows.append(key)
            pGrid.append(pRows)
        return pGrid

    def countGrid(self, isPart2: Optional[bool] = False) -> int:
        loops = 2 if self.useTest else 5
        if isPart2 and not self.useTest:
            loops = 18
        gridKey = []
        print(loops)
        for i in range(loops):
            print(i)
            divisor = 2 if self.size % 2 == 0 else 3
            gridKey = self.getKeys(divisor)
            newGrid = self.increaseGrid(gridKey)
            self.updateGrid(newGrid, divisor)
            self.size = len(self.grid)

        return sum(x == "#" for row in self.grid for x in row)


if __name__ == "__main__":
    gpu = GPU()
    print("Day 21 part 1:", gpu.countGrid())
    print("Day 21 part 2:", gpu.countGrid(True))
