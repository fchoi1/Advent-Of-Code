from typing import List, Optional, Tuple


class Dish:
    def getInput(self) -> List[List[List[str]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(x.strip()) for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.rocks = self.getInput()
        self.rows = len(self.rocks)
        self.cols = len(self.rocks[0])
        self.dir = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        self.ranges = [
            (range(self.rows), range(self.cols)),
            (range(self.cols), range(self.rows)),
            (range(self.rows - 1, -1, -1), range(self.cols)),
            (range(self.cols - 1, -1, -1), range(self.rows)),
        ]

    def moveRock(self, pos: Tuple[int], direction: int) -> None:
        x, y = pos
        dx, dy = self.dir[direction]
        while 0 <= y < self.rows and 0 <= x < self.cols and self.rocks[y][x] == ".":
            y += dy
            x += dx
        self.rocks[y - dy][x - dx] = "O"

    def shift(self, iRange: List[int], jRange: List[int], direction: int) -> None:
        for i in iRange:
            for j in jRange:
                x, y = (i, j) if direction in [1, 3] else (j, i)
                if self.rocks[y][x] == "O":
                    self.rocks[y][x] = "."
                    self.moveRock((x, y), direction)

    def getScore(self) -> int:
        total = 0
        for y, row in enumerate(self.rocks[::-1]):
            total += (y + 1) * sum(char == "O" for char in row)
        return total

    def getTotal(self) -> int:
        loops = 1_000_000_000
        scores = []
        scoresSet = {}
        prev = []
        for i in range(loops):
            for j in range(4):
                self.shift(*self.ranges[j], j)
            s = self.getScore()
            scores.append(s)
            prev.append(s)
            if len(scores) < 5:
                continue
            key = ",".join(map(str, prev))
            if key in scoresSet:
                break
            scoresSet[key] = i
            prev = prev[1:]

        index = scoresSet[key] - 1
        cycle = i - index
        remain = (loops - index) % cycle
        return scores[index : index + cycle][remain]

    def getOneShift(self):
        self.shift(*self.ranges[0], 0)
        return self.getScore()


if __name__ == "__main__":
    dish = Dish()
    print("Day 14 part 1:", dish.getOneShift())
    print("Day 14 part 2:", dish.getTotal())
