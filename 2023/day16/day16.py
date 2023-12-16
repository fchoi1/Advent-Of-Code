from typing import List, Optional, Tuple, Set


class Lava:
    def getInput(self) -> List[List[List[str]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(x.strip()) for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()
        self.w = len(self.map[0])
        self.h = len(self.map)

    def inBounds(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def moveBeam(
        self,
        d: Tuple[int],
        pos: Tuple[int],
        seen: Set[Tuple[int]],
        energy: Set[Tuple[int]],
    ):
        dx, dy = d
        x, y = pos
        if (x, y, d) in seen:
            return seen, energy
        seen.add((x, y, d))
        while self.inBounds(x, y) and self.map[y][x] == ".":
            energy.add((x, y))
            x, y = x + dx, y + dy

        if not self.inBounds(x, y):
            return seen, energy
        energy.add((x, y))
        sym = self.map[y][x]

        for d, p in self.getMoveList(sym, d, (x, y)):
            seen, energy = self.moveBeam(d, p, seen, energy)
        return seen, energy

    def getMoveList(self, sym: str, d: Tuple[int], pos: Tuple[int]):
        m = []
        dx, dy = d
        x, y = pos
        if dy == 0:
            if sym == "-":
                m.append((d, (x + dx, y)))
            elif sym == "/" and dx == 1 or sym == "\\" and dx == -1:
                m.append(((0, -1), (x, y - 1)))
            elif sym == "/" and dx == -1 or sym == "\\" and dx == 1:
                m.append(((0, 1), (x, y + 1)))
            elif sym == "|":
                m.append(((0, 1), (x, y + 1)))
                m.append(((0, -1), (x, y - 1)))
        else:
            if sym == "|":
                m.append((d, (x, y + dy)))
            elif sym == "/" and dy == 1 or sym == "\\" and dy == -1:
                m.append(((-1, 0), (x - 1, y)))
            elif sym == "/" and dy == -1 or sym == "\\" and dy == 1:
                m.append(((1, 0), (x + 1, y)))
            elif sym == "-":
                m.append(((-1, 0), (x - 1, y)))
                m.append(((1, 0), (x + 1, y)))
        return m

    def getE(
        self,
        direction: Optional[Tuple[int, int]] = (1, 0),
        start: Optional[Tuple[int, int]] = (0, 0),
    ) -> int:
        return len(self.moveBeam(direction, start, set(), set())[1])

    def getMax(self):
        t = 0
        for i in range(len(self.map)):
            t = max(t, self.getE((0, 1), (i, 0)), self.getE((0, -1), (i, self.h - 1)))
        for i in range(len(self.map[0])):
            t = max(t, self.getE((1, 0), (0, i)), self.getE((-1, 0), (self.w - 1, i)))
        return t


if __name__ == "__main__":
    lava = Lava()
    print("Day 16 part 1:", lava.getE())
    print("Day 16 part 2:", lava.getMax())
    # Total runtime ~1.67s
