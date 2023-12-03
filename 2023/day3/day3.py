from typing import List, Optional, Set, Tuple


class Cube:
    def getInput(self) -> List[List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(x.strip()) for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.engines = self.getInput()
        self.dirMap = [
            [0, 1],
            [0, -1],
            [1, 1],
            [-1, 1],
            [1, 0],
            [-1, 0],
            [-1, -1],
            [1, -1],
        ]
        self.total = 0
        self.gear = 0
        self.checkEngine()

    def checkNum(self, x: int, y: int, seen: Set[Tuple[int]]) -> int:
        char, num = self.engines[y][x], ""
        while char in "0123456789":
            x -= 1
            char = self.engines[y][x]
        x += 1
        char = self.engines[y][x]
        if (x, y) in seen:
            return 0
        seen.add((x, y))
        while char in "0123456789":
            num += char
            x += 1
            if x >= len(self.engines[0]):
                return int(num)
            char = self.engines[y][x]
        return int(num)

    def checkAround(self, x: int, y: int):
        total = 0
        nums = []
        seen = set()
        for dx, dy in self.dirMap:
            newX, newY = dx + x, dy + y
            char = self.engines[newY][newX]
            if (
                0 <= newX < len(self.engines[0])
                and 0 <= newY < len(self.engines)
                and char in "0123456789"
            ):
                n = self.checkNum(newX, newY, seen)
                if n != 0:
                    nums.append(n)
                    total += n
        gr = nums[0] * nums[1] if len(nums) == 2 else 0
        self.total += total
        self.gear += gr if self.engines[y][x] == "*" else 0

    def checkEngine(self) -> None:
        for j, row in enumerate(self.engines):
            for i, char in enumerate(row):
                if char not in "0123456789.":
                    self.checkAround(i, j)

    def getTotal(self) -> int:
        return self.total

    def getGearRatio(self) -> int:
        return self.gear


if __name__ == "__main__":
    cube = Cube()
    print("Day 3 part 1:", cube.getTotal())
    print("Day 3 part 2:", cube.getGearRatio())
