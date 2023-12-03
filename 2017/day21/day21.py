from typing import Optional, Dict, List


class GPU:
    def getInput(self) -> Dict[str, str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        enhance = {}
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip().split(" => ")
                enhance[line[0]] = line[1]
        return enhance

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.particles = self.getInput()
        self.updatePermutations()
        self.grid = [".#.", "..#", "###"]

    def updatePermutations(self) -> None:
        temp = self.particles.copy()
        for key, val in temp.items():
            rows = [list(x) for x in key.split("/")]
            for _ in range(4):
                rotated = self.rotate(rows)
                flipped = rotated[::-1]
                self.particles[self.generateKey(rotated)] = val
                self.particles[self.generateKey(flipped)] = val
                rows = rotated

    def rotate(self, tile: List[List[str]]) -> str:
        return [list(row) for row in zip(*reversed(tile))]

    def generateKey(self, tile: List[List[str]]) -> str:
        return "/".join("".join(row) for row in tile)

    def findMatch(self, rowStr: int) -> str:
        if rowStr in self.particles:
            return self.particles[rowStr]
        else:
            return ""

    def updateGrid(self, grid: List[List[str]], size: int) -> None:
        self.grid = [
            "".join([string.split("/")[i] for string in row])
            for row in grid
            for i in range(size + 1)
        ]

    def increaseGrid(self, grid: List[List[str]]) -> List[List[str]]:
        return [[self.findMatch(string) for string in row] for row in grid]

    def getKeys(self, size: int) -> List[List[str]]:
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
        self.grid = [".#.", "..#", "###"]
        loops = 2 if self.useTest else 5
        if isPart2 and not self.useTest:
            loops = 18
        gridKey = []
        for _ in range(loops):
            divisor = 2 if len(self.grid) % 2 == 0 else 3
            gridKey = self.getKeys(divisor)
            newGrid = self.increaseGrid(gridKey)
            self.updateGrid(newGrid, divisor)
        return sum(x == "#" for row in self.grid for x in row)


if __name__ == "__main__":
    gpu = GPU()
    print("Day 21 part 1:", gpu.countGrid())
    print("Day 21 part 2:", gpu.countGrid(True))
    # Total runtime ~1.4s
