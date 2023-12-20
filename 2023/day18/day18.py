from typing import List, Optional, Tuple


class Lava:
    def getInput(self) -> List[Tuple[int, str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        cmd = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                dir_, steps, color = line.split()
                newSteps = color[2:-2]
                newDir = color[-2:-1]
                cmd.append((dir_, int(steps), int(newDir), int(newSteps, 16)))
            return cmd

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.cmd = self.getInput()
        self.dirMap = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def det(self, pos1: List[int], pos2: List[int]) -> int:
        return pos1[0] * pos2[1] - pos2[0] * pos1[1]

    def getTotal(self, isPart2: Optional[bool] = False) -> int:
        x, y, total = 0, 0, 0
        for dir_, steps, newDir, newSteps in self.cmd:
            direction = newDir if isPart2 else "RDLU".index(dir_)
            s = newSteps if isPart2 else steps
            dx, dy = self.dirMap[direction]
            total += self.det((x, y), (x + (dx * s), y + (dy * s))) + s
            x, y = x + (dx * s), y + (dy * s)
        return int(total / 2 + 1)


if __name__ == "__main__":
    lava = Lava()
    print("Day 18 part 1:", lava.getTotal())
    print("Day 18 part 2:", lava.getTotal(True))
