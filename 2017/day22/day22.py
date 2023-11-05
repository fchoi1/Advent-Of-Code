from typing import Optional, Set, Tuple, List


class Virus:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(x.strip()) for x in file1.readlines()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.grid = self.getInput()
        self.start = (len(self.grid) // 2, len(self.grid) // 2)
        self.initialInfected = sum(node == "#" for row in self.grid for node in row)

    def reset(self):
        self.infected = self.createSet()
        self.weakend = set()
        self.flagged = set()

    def createSet(self) -> Set[Tuple[int]]:
        infected = set()
        for j in range(len(self.grid)):
            for i in range(len(self.grid)):
                if self.grid[j][i] == "#":
                    infected.add((i, j))
        return infected

    def countBursts(self, isPart2: Optional[bool] = False) -> int:
        self.reset()
        dirList = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        direction = burst = 0
        loops = 10_000_000 if isPart2 else 10_000
        node = self.start
        for _ in range(loops):
            if node in self.weakend:
                self.weakend.remove(node)
                self.infected.add(node)
                burst += 1
            elif node in self.flagged:
                self.flagged.remove(node)
                direction += 2
            elif node in self.infected:
                self.flagged.add(node) if isPart2 else self.infected.remove(node)
                direction += 1
            else:
                if isPart2:
                    self.weakend.add(node)
                else:
                    self.infected.add(node)
                    burst += 1
                direction -= 1
            dx, dy = dirList[direction % 4]
            node = (node[0] + dx, node[1] + dy)
        return burst


if __name__ == "__main__":
    virus = Virus()
    print("Day 22 part 1:", virus.countBursts())
    print("Day 22 part 2:", virus.countBursts(True))
    # Total runtime ~5 seconds
