from typing import List, Optional, Tuple, Dict


class Aplenty:

    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(row.strip()) for row in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()
        self.rocks = 0
        self.getStart()

    def getStart(self):
        for j, row in enumerate(self.map):
            for i, char in enumerate(row):
                if char == "S":
                    self.sx, self.sy = i, j
                if char == "#":
                    self.rocks += 1

    def inBounds(self, pos: Tuple[int]) -> bool:
        return 0 <= pos[0] < len(self.map[0]) and 0 <= pos[1] < len(self.map)

    def printGrid(self, possible):
        print()
        for j in range(len(self.map)):
            row = ""
            for i in range(len(self.map[0])):
                if self.map[j][i] == "#":
                    row += "#"
                elif (i, j) in possible:
                    row += "0"
                else:
                    row += "."
            print(row)

    def bfs(self, start, target=None):
        count = 0
        q = [start]
        seen = set()
        step = 0
        possible = set()
        while q:
            temp = []
            for pos in q:
                x, y = pos
                if pos in seen:
                    continue
                seen.add(pos)
                if step % 2 == 0:
                    count += 1
                    possible.add(pos)
                for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                    newPos = (x + dx, y + dy)
                    if self.inBounds(newPos) and self.map[newPos[1]][newPos[0]] != "#":
                        temp.append(newPos)
            if target and step == target:
                break
            step += 1
            q = temp
        # self.printGrid(possible)
        print(count, len(possible))
        return count

    def getTotal(self) -> int:
        target = 7 if self.useTest else 65
        return self.bfs((self.sx, self.sy), target)

    def getTotal2(self) -> int:
        size = len(self.map)
        print(self.sx, self.sy)
        oddCount = self.bfs((self.sx, self.sy))
        evenCount = self.bfs((self.sx + 1, self.sy))

        ss = size // 2
        small_tl = self.bfs((size - 1, size - 1), ss)
        small_tr = self.bfs((0, size - 1), ss)
        small_bl = self.bfs((size - 1, 0), ss)
        small_br = self.bfs((0, 0), ss)

        bs = 3 * size // 2
        big_tl = self.bfs((size - 1, size - 1), bs)
        big_tr = self.bfs((0, size - 1), bs)
        big_bl = self.bfs((size - 1, 0), bs)
        big_br = self.bfs((0, 0), bs)

        step = size

        top = self.bfs((self.sx, size - 1), step)
        bot = self.bfs((self.sx, 0), step)
        left = self.bfs((size - 1, self.sy), step)
        right = self.bfs((0, self.sy), step)

        # assumptions
        # step size ends in center of grid, grid is square
        # diamond shape

        # steps = 458
        steps = 26501365
        gridWidth = steps // size
        odd = gridWidth**2
        even = (gridWidth - 1) ** 2
        # print(odd, oddCount, even, evenCount, len(self.map))
        # print((top, bot, left, right), (top + bot + left + right))
        print(
            big_tl,
            big_tr,
            big_bl,
            big_br,
            (gridWidth - 1),
            (big_tl + big_tr + big_bl + big_br),
        )
        print(
            (small_tl, small_tr, small_bl, small_br),
            gridWidth,
            (small_tl + small_tr + small_bl + small_br),
        )
        total = (
            odd * oddCount
            + even * evenCount
            + (gridWidth - 1) * (big_tl + big_tr + big_bl + big_br)
            + gridWidth * (small_tl + small_tr + small_bl + small_br)
            + (top + bot + left + right)
        )
        # 605 247 150 336 695
        # 605 247 138 198 755
        # 605 245 620 752 677
        #  6504 6515 6505 6494
        # (6492, 6472, 6496, 6498) 202299 25958

        return total

        pass


if __name__ == "__main__":
    aplenty = Aplenty()
    # print("Day 19 part 1:", aplenty.getTotal())
    print("Day 19 part 2:", aplenty.getTotal2())
    # Total Runtime ~1.6s
