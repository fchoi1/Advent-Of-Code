from typing import List, Optional


class Spiral:
    def getInput(self) -> int:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return int(file1.readline().strip())

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.num = self.getInput()
        self.rows = 11

    def getTotal(self, grid: List[List[int]], index: List[int]) -> int:
        adjDir = [(0, 1), (1, 1), (-1, 1), (0, -1), (1, -1), (-1, -1), (-1, 0), (1, 0)]
        total = 0
        for dx, dy in adjDir:
            newX, newY = dx + index[0], dy + index[1]
            if 0 <= newX < len(grid[0]) and 0 <= newY < len(grid):
                total += grid[newY][newX]
        return total

    def getShortestDistance(self) -> int:
        loop = val = partition = 0
        while val < self.num:
            loop += 1
            val = (2 * loop + 1) ** 2
        partition = 2 * loop
        for _ in range(8):
            if val - partition <= self.num <= val:
                return abs(abs(self.num - val) - partition // 2) + loop
            val -= partition
        return -1

    def getNextAdjacent(self) -> int:
        grid = [[0 for _ in range(self.rows)] for _ in range(self.rows)]
        grid[self.rows // 2][self.rows // 2] = 1
        index = [self.rows // 2, self.rows // 2]
        dirList = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        loop = direction = 0
        count = 1
        corner = 2
        while True:
            while count < corner:
                index[0] += dirList[direction][0]
                index[1] += dirList[direction][1]

                grid[index[1]][index[0]] = self.getTotal(grid, index)
                if grid[index[1]][index[0]] > self.num:
                    return grid[index[1]][index[0]]
                count += 1
            direction = (direction + 1) % 4
            if direction == 1:
                loop += 1
                partition = 2 * loop
                corner = (2 * loop + 1) ** 2 - (partition) * 3
            else:
                corner += partition + int(direction == 0)


if __name__ == "__main__":
    Spiral = Spiral()
    print("Day 3 part 1:", Spiral.getShortestDistance())
    print("Day 3 part 2:", Spiral.getNextAdjacent())
