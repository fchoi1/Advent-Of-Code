import sys

sys.path.insert(0, "..")
from day10.day10 import Knot
from typing import Optional, List


class Defragmentation:
    def getInput(self) -> str:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return file1.readline().strip()

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.key = self.getInput()
        self.length = 128
        self.knot = Knot()
        self.disk = []
        self.generateHashes()

    def getBinHash(self, knotHash: str) -> str:
        binaryStr = ""
        for char in knotHash:
            binaryStr += "{:04b}".format(int(char, 16))
        return binaryStr

    def generateHashes(self) -> None:
        self.count = 0
        for i in range(self.length):
            hashKey = self.key + "-" + str(i)
            knotHash = self.knot.generateKnotHash(hashKey)
            binary = self.getBinHash(knotHash)
            self.disk.append(list(binary))
            self.count += binary.count("1")

    def getUsed(self) -> int:
        return self.count

    def isValid(self, x: int, y: int) -> bool:
        return 0 <= x < self.length and 0 <= y < self.length and self.disk[y][x] == "1"

    def getRegions(self) -> int:
        regions = 0
        visited = set()

        def dfs(pos: List[int]):
            if pos in visited:
                return
            visited.add(pos)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                newX, newY = pos[0] + dx, pos[1] + dy
                if self.isValid(newX, newY):
                    dfs((newX, newY))

        for j in range(self.length):
            for i in range(self.length):
                if (i, j) not in visited and self.disk[j][i] == "1":
                    regions += 1
                    dfs((i, j))
        return regions


if __name__ == "__main__":
    defragmentation = Defragmentation(True)
    print("Day 14 part 1:", defragmentation.getUsed())
    print("Day 14 part 2:", defragmentation.getRegions())
