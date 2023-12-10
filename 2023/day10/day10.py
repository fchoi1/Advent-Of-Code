from typing import List, Optional, Set, Tuple


class Mirage:
    def getInput(self) -> List[List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(s.strip()) for s in file1]

    def __init__(
        self, useTest: Optional[bool] = False, checkOpposite: Optional[bool] = False
    ) -> None:
        self.useTest = useTest
        # change this depending on which side to check
        self.checkOpposite = checkOpposite
        self.map = self.getInput()
        self.dirMap = [
            [0, 1],
            [1, 0],
            [0, -1],
            [-1, 0],
        ]  # down, right, up, left - counter clockwise
        self.trans = ["down", "right", "up", "left"]
        self.charMap = {
            "L": [(1, 1), (2, -1)],
            "|": [(0, 0), (2, 0)],
            "-": [(1, 0), (3, 0)],
            "J": [(2, 1), (3, -1)],
            "7": [(0, -1), (3, 1)],
            "F": [(0, 1), (1, -1)],
        }
        self.loop = set()
        self.rotate, self.start = self.getStart()
        self.furthest, self.holes = 0, 0
        self.runLoop()

    def getStart(self):
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == "S":
                    exits = []
                    for n, (dx, dy) in enumerate(self.dirMap):
                        newX, newY = dx + x, dy + y
                        if self.inBounds(newX, newY):
                            if self.map[newY][newX] in ["|LJ", "-J7", "|7F", "-LF"][n]:
                                exits.append(n)
                    for key, dirs in self.charMap.items():
                        if exits[0] == dirs[0][0] and exits[1] == dirs[1][0]:
                            self.map[y][x] = key
                            rotate = dirs[0][0] + 1 if key in "LFJ7" else dirs[0][0]
                            return rotate, (x, y)

    def inBounds(self, x, y):
        return 0 <= x < len(self.map[0]) and 0 <= y < len(self.map)

    def runLoop(self):
        pos = self.start
        steps = 0
        checkDfs = set()
        flip = 1 if self.checkOpposite else -1
        while pos not in self.loop:
            self.loop.add(pos)
            x, y = pos
            currChar = self.map[y][x]

            cX = self.dirMap[(self.rotate + flip) % 4][0] + pos[0]
            cY = self.dirMap[(self.rotate + flip) % 4][1] + pos[1]
            if (cX, cY) not in self.loop and self.inBounds(cX, cY):
                checkDfs.add((cX, cY))

            for i, r in self.charMap[currChar]:
                dx, dy = self.dirMap[i]
                newX, newY = dx + x, dy + y
                if self.inBounds(newX, newY) and (newX, newY) not in self.loop:
                    self.rotate += r
                    cX = self.dirMap[(self.rotate + flip) % 4][0] + pos[0]
                    cY = self.dirMap[(self.rotate + flip) % 4][1] + pos[1]
                    if (cX, cY) not in self.loop:
                        checkDfs.add((cX, cY))
                    pos = (newX, newY)
                    break
            if pos in checkDfs:
                checkDfs.discard(pos)
            steps += 1
        self.furthest = steps // 2 + 1
        self.holes = self.checkDfs(checkDfs)

    def checkDfs(self, check: Set[Tuple[int]]) -> int:
        visited = set()
        for pos in check:
            if pos not in visited:
                self.dfs(visited, pos)
        return len(visited)

    def dfs(self, visited: Set[Tuple[int]], pos: Tuple[int]) -> None:
        if pos in visited or pos in self.loop:
            return
        visited.add(pos)
        for dx, dy in self.dirMap:
            newX, newY = dx + pos[0], dy + pos[1]
            if self.inBounds(newX, newY):
                self.dfs(visited, (newX, newY))

    def getFurthest(self) -> int:
        return self.furthest

    def getHoles(self) -> int:
        return self.holes


if __name__ == "__main__":
    mirage = Mirage()
    print("Day 9 part 1:", mirage.getFurthest())
    print("Day 9 part 2:", mirage.getHoles())
