from typing import List, Optional, Tuple, Dict
from math import lcm


class Blizzard:
    def getInput(self) -> List[str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(x.strip()) for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()

        self.width = len(self.map[0]) - 2
        self.height = len(self.map) - 2

        self.directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]

        self.start, self.finish = self.getStartAndFinish()
        self.blizzards = self.getBlizzards()

        self.lcm = lcm(self.width, self.height)

    def getStartAndFinish(self) -> List[Tuple[int, int] | None]:
        start = finish = None
        for y, row in enumerate(self.map):
            for x, val in enumerate(row):
                if (y in [0, len(self.map) - 1] or x in [0, len(row) - 1]) and val == ".":
                    if not start:
                        start = (x, y)
                    else:
                        finish = (x, y)
                        return [start, finish]
        return [start, finish]

    def getBlizzards(self) -> Dict:
        blizzards = tuple(set() for _ in range(4))
        for y, row in enumerate(self.map):
            for x, val in enumerate(row):
                if val in "><v^":
                    blizzards["><v^".index(val)].add((x, y))
        return blizzards

    def getFewestMinutes(self) -> int:
        return self.getShortest(self.start)

    def getRoundTrip(self) -> Dict:
        time = 0
        for _ in range(3):
            time = self.getShortest(self.start, time)
            self.start, self.finish = self.finish, self.start
        return time

    # use bfs
    def getShortest(self, start: Tuple[int], time: Optional[int] = 0) -> int:
        q = [start]
        visited = set()

        while q:
            tempQ = []
            for currPos in q:
                if currPos == self.finish:
                    return time

                state = currPos + ((time) % self.lcm,)
                if self.hitBlizzards(currPos, time) or state in visited:
                    continue

                visited.add(state)

                for dx, dy in self.directions:
                    if self.isInBounds(currPos[0] + dx, currPos[1] + dy):
                        newPos = (currPos[0] + dx, currPos[1] + dy)
                        tempQ.append(newPos)
            time += 1
            q = tempQ
        return -1

    def hitBlizzards(self, currPos: Tuple[int], minute: int) -> bool:
        x, y = currPos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        if currPos == self.start:
            return False

        for i, (dx, dy) in enumerate(directions):
            xBlizz = (x - dx * minute) % (self.width)
            yBlizz = (y - dy * minute) % (self.height)

            if xBlizz < 1:
                xBlizz = self.width

            if yBlizz < 1:
                yBlizz = self.height

            if (xBlizz, yBlizz) in self.blizzards[i]:
                return True
        return False

    def isInBounds(self, x: int, y: int) -> bool:
        if (x, y) in [self.start, self.finish]:
            return True
        return 1 <= x <= self.width and 1 <= y <= self.height


if __name__ == "__main__":
    blizzard = Blizzard()
    print("Day 24 part 1:", blizzard.getFewestMinutes())
    print("Day 24 part 2:", blizzard.getRoundTrip())
    # Runtime ~3 seconds
