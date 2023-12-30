from typing import List, Optional, Tuple, Set


class Walk:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(x.strip()) for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()
        self.w = len(self.map[0])
        self.h = len(self.map)
        self.dirMap = {
            "v": (0, 1),
            "^": (0, -1),
            "<": (-1, 0),
            ">": (1, 0),
        }
        self.start = (1, 0)
        self.end = (self.w - 2, self.h - 1)
        self.length = 0
        self.cache = {}

    def inBounds(self, x, y) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h

    def runRoute(self, prevPos: Tuple[int], pos: Tuple[int]) -> Tuple[Tuple[int] | int]:
        x, y = pos
        prevX, prevY = prevPos
        routes = [pos]
        steps = 0
        while True:
            x, y = routes[0]
            routes = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                newX, newY = x + dx, y + dy
                if (
                    self.inBounds(newX, newY)
                    and (newX, newY) != (prevX, prevY)
                    and self.map[newY][newX] != "#"
                ):
                    routes.append((newX, newY))
            if len(routes) != 1:
                return ((prevX, prevY), (x, y), steps)
            steps += 1
            prevX, prevY = x, y

    def dfs(self, p2: bool, pos: Tuple[int], seen: Set[Tuple[int]], steps: int) -> None:
        if pos == self.end:
            print(steps, self.length)
            self.length = max(self.length, steps)
            return
        if pos in seen:
            return
        prev = None
        seen.add(pos)
        steps += 1
        x, y = pos
        if not p2 and self.map[y][x] in "<>^v":
            dx, dy = self.dirMap[self.map[y][x]]
            self.dfs(p2, (x + dx, y + dy), seen, steps)
            return
        routes = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newX, newY = x + dx, y + dy
            if (
                self.inBounds(newX, newY)
                and (newX, newY) not in seen
                and self.map[newY][newX] != "#"
            ):
                routes.append((newX, newY))
        if len(routes) == 1:
            if routes[0] not in self.cache:
                prev, p, s = self.runRoute(pos, routes[0])
                self.cache[routes[0]] = prev, p, s
            else:
                prev, p, s = self.cache[routes[0]]
            seen.add(prev)
            self.dfs(p2, p, seen, steps + s)
        elif len(routes) > 1:
            for r in routes:
                self.dfs(p2, r, seen, steps)
        if prev:
            seen.remove(prev)
        seen.remove(pos)

    def getTotal(self, isPart2: Optional[bool] = False) -> int:
        self.seen = set()
        self.dfs(isPart2, self.start, set(), 0)
        return self.length


if __name__ == "__main__":
    walk = Walk()
    print("Day 23 part 1:", walk.getTotal())
    print("Day 23 part 2:", walk.getTotal(True))
    # Total Runtime
