from typing import List, Optional, Tuple


class StepCounter:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(row.strip()) for row in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()
        self.getStart()

    def getStart(self) -> None:
        for j, row in enumerate(self.map):
            for i, char in enumerate(row):
                if char == "S":
                    self.sx, self.sy = i, j

    def inBounds(self, pos: Tuple[int]) -> bool:
        return 0 <= pos[0] < len(self.map[0]) and 0 <= pos[1] < len(self.map)

    def bfs(self, start: List[Tuple[int]], target: Optional[int] = None) -> int:
        count, step = 0, 0
        q = start
        seen = set()
        while q:
            temp = []
            for pos in q:
                x, y = pos
                if pos in seen:
                    continue
                seen.add(pos)
                if step % 2 == 0:
                    count += 1
                for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                    newPos = (x + dx, y + dy)
                    if self.inBounds(newPos) and self.map[newPos[1]][newPos[0]] != "#":
                        temp.append(newPos)
            if target and step == target:
                break
            step += 1
            q = temp
        return count

    def getSteps(self) -> int:
        return self.bfs([(self.sx, self.sy)], 7 if self.useTest else 65)

    def getSteps2(self) -> int:
        size = len(self.map)
        oddCount = self.bfs([(self.sx, self.sy)])
        evenCount = self.bfs([(self.sx + 1, self.sy)])

        ss = size // 2
        small_tl = self.bfs([(size - 1, size - 1)], ss)
        small_tr = self.bfs([(0, size - 1)], ss)
        small_bl = self.bfs([(size - 1, 0)], ss)
        small_br = self.bfs([(0, 0)], ss)

        # even case
        bs = 3 * size // 2 - 1
        big_tl = self.bfs([(size - 1, size - 2), (size - 2, size - 1)], bs)
        big_tr = self.bfs([(0, size - 2), (1, size - 1)], bs)
        big_bl = self.bfs([(size - 2, 0), (size - 1, 1)], bs)
        big_br = self.bfs([(0, 1), (1, 0)], bs)

        top = self.bfs([(self.sx, size - 1)], size)
        bot = self.bfs([(self.sx, 0)], size)
        left = self.bfs([(size - 1, self.sy)], size)
        right = self.bfs([(0, self.sy)], size)

        steps = 5000 if self.useTest else 26501365
        gridWidth = steps // size
        odd = gridWidth**2
        even = (gridWidth - 1) ** 2
        return (
            odd * oddCount
            + even * evenCount
            + (gridWidth - 1) * (big_tl + big_tr + big_bl + big_br)
            + gridWidth * (small_tl + small_tr + small_bl + small_br)
            + (top + bot + left + right)
        )


if __name__ == "__main__":
    stepCounter = StepCounter()
    print("Day 21 part 1:", stepCounter.getSteps())
    print("Day 21 part 2:", stepCounter.getSteps2())
