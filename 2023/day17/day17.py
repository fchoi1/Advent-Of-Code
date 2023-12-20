from typing import List, Optional
import heapq


class Lava:
    def getInput(self) -> List[List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(map(int, x.strip())) for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()
        self.H = len(self.map)
        self.W = len(self.map[0])
        self.dirMap = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def inBounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.W and 0 <= y < self.H

    def dijkstra(self, minSteps: int, maxSteps: int) -> int:
        q = [(0, 0, 0, 1), (0, 0, 0, 0)]
        seen = set()
        while q:
            heat, x, y, d = heapq.heappop(q)
            if (x, y, d) in seen:
                continue
            seen.add((x, y, d))
            if (x, y) == (self.W - 1, self.H - 1):
                return heat
            for i in [d - 1, d + 1]:
                i = i % 4
                newX, newY, newHeat = x, y, heat
                dx, dy = self.dirMap[i]
                for s in range(0, maxSteps):
                    newX, newY = newX + dx, newY + dy
                    if self.inBounds(newX, newY):
                        newHeat += self.map[newY][newX]
                        if minSteps <= s < maxSteps:
                            heapq.heappush(q, (newHeat, newX, newY, i))

    def minHeatLoss(self, isPart2: Optional[bool] = False) -> int:
        minSteps = 3 if isPart2 else 0
        maxSteps = 10 if isPart2 else 3
        return self.dijkstra(minSteps, maxSteps)


if __name__ == "__main__":
    lava = Lava()
    print("Day 17 part 1:", lava.minHeatLoss())
    print("Day 17 part 2:", lava.minHeatLoss(True))
    # Total runtime ~ 2.75s
