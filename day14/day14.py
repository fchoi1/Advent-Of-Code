from typing import List, Optional, Tuple


class Cave:
    def getInput(self) -> List[Tuple[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
            data = []
            self.maxY = self.maxX = float("-inf")
            self.minX = float("inf")
            self.minY = 0

            for line in Lines:
                elements = line.split("->")
                tuples_list = []
                for element in elements:
                    coordinates = element.strip().split(",")
                    coordinates = [int(coord) for coord in coordinates]

                    if coordinates[0] > self.maxX:
                        self.maxX = coordinates[0]
                    if coordinates[1] > self.maxY:
                        self.maxY = coordinates[1]
                    if coordinates[0] < self.minX:
                        self.minX = coordinates[0]
                    if coordinates[1] < self.minY:
                        self.minY = coordinates[1]

                    tuple_value = tuple(coordinates)
                    tuples_list.append(tuple_value)
                data.append(tuples_list)
            return data

    def createGrid(self, height: int, width: int) -> List[List[str]]:
        return [["." for _ in range(width + 1)] for _ in range(height + 1)]

    def populateGrid(
        self, grid: List[List[str]], minX: int, addFloor: bool = False
    ) -> None:
        for lines in self.inputData:
            (prevX, prevY) = lines[0]
            for x, y in lines[1:]:
                if prevX == x:
                    for i in range(abs(prevY - y) + 1):
                        tempY = prevY - (prevY - y) / abs(prevY - y) * i
                        tempX = x - minX
                        grid[int(tempY)][tempX] = "X"
                elif prevY == y:
                    for i in range(abs(prevX - x) + 1):
                        tempY = y
                        tempX = prevX - (prevX - x) / abs(prevX - x) * i - minX
                        grid[tempY][int(tempX)] = "X"
                prevX = x
                prevY = y
            if addFloor:
                height = len(grid) - 1
                grid[height] = ["X" for _ in grid[height]]
        return grid

    def printGrid(
        self, grid: List[List[str]], startX: int = -1, endX: int = -1
    ) -> None:
        for row in grid:
            if startX == -1 or endX == -1:
                print(row)
            else:
                print(row[startX:endX])

    def countSand1(self) -> int:
        sandPos = self.defaultSandDrop
        self.grid1[sandPos[1]][sandPos[0]] = "+"
        while 0 <= sandPos[0] <= self.width and 0 <= sandPos[1] < self.height:
            if self.dropSand(self.grid1, sandPos) == sandPos:
                self.stableSand += 1
                self.grid1[sandPos[1]][sandPos[0]] = "O"
                sandPos = self.defaultSandDrop
            else:
                sandPos = self.dropSand(self.grid1, sandPos)
        return self.stableSand

    def countSand2(self) -> int:
        sandPos = self.defaultSandDrop2
        self.grid2[sandPos[1]][sandPos[0]] = "+"
        while self.dropSand(self.grid2, sandPos) != self.defaultSandDrop2:
            if self.dropSand(self.grid2, sandPos) == sandPos:
                self.stableSand2 += 1
                self.grid2[sandPos[1]][sandPos[0]] = "O"
                sandPos = self.defaultSandDrop2
            else:
                sandPos = self.dropSand(self.grid2, sandPos)
        self.stableSand2 += 1
        return self.stableSand2

    def dropSand(self, grid: List[List[str]], sandPos: List[int]) -> List[int]:
        [sandPosX, sandPosY] = sandPos
        if grid[sandPosY + 1][sandPosX] == ".":
            sandPosY += 1
        elif grid[sandPosY + 1][sandPosX - 1] == ".":
            sandPosY += 1
            sandPosX -= 1
        elif grid[sandPosY + 1][sandPosX + 1] == ".":
            sandPosY += 1
            sandPosX += 1
        return [sandPosX, sandPosY]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        """Main entry point of the app"""
        self.useTest = useTest
        self.inputData = self.getInput()

        self.height = self.maxY - self.minY
        self.width = self.maxX - self.minX

        self.width2 = self.maxX

        self.stableSand = 0
        self.stableSand2 = 0
        self.defaultSandDrop = [500 - self.minX, 0]
        self.defaultSandDrop2 = [500, 0]

        self.grid1 = self.createGrid(self.height, self.width)
        self.grid2 = self.createGrid(self.height + 2, self.width2 + 200)

        self.grid1 = self.populateGrid(self.grid1, self.minX)
        self.grid2 = self.populateGrid(self.grid2, 0, True)


if __name__ == "__main__":
    """This is executed when run from the command line"""
    cave = Cave(False)
    print("Day 14 part 1:", cave.countSand1())
    print("Day 14 part 2:", cave.countSand2())
