from typing import Optional, List


class Tubes:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        tubeMap = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                line = line.replace("\n", "")
                tubeMap.append(list(line))
        return tubeMap

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.tubeMap = self.getInput()
        self.steps = 0
        self.path = ""
        self.runPath()

    def runPath(self) -> str:
        for i, char in enumerate(self.tubeMap[0]):
            if char == "|":
                break
        x, y = i, 0
        Dx, Dy = 0, 1
        while self.tubeMap[y][x] != " ":
            if self.tubeMap[y][x] == "+":
                for Dx, Dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    tmpY = y + Dy
                    tmpX = x + Dx
                    if not self.inBounds(tmpX, tmpY):
                        continue
                    if (
                        self.tubeMap[tmpY][tmpX] != " "
                        and tmpY != prevY
                        and tmpX != prevX
                    ):
                        break
            elif self.tubeMap[y][x] not in "-+|":
                self.path += self.tubeMap[y][x]
            prevX, prevY = x, y
            x += Dx
            y += Dy
            self.steps += 1

    def inBounds(self, x: int, y: int) -> bool:
        return 0 <= x < len(self.tubeMap[0]) and 0 <= y < len(self.tubeMap)

    def getPath(self) -> str:
        return self.path

    def getSteps(self) -> int:
        return self.steps


if __name__ == "__main__":
    tubes = Tubes(True)
    print("Day 19 part 1:", tubes.getPath())
    print("Day 19 part 1:", tubes.getSteps())
