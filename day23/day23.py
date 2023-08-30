from typing import List, Optional, Set


class Elves:
    def getInput(self) -> List[str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                data.append(list(line.strip()))
            return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.map = self.getInput()

        self.positions = self.getPositions(self.map)
        self.directions = ["N", "S", "W", "E"]
        self.dirMap = {
            "E": [(1, 0), (1, 1), (1, -1)],
            "S": [(0, 1), (1, 1), (-1, 1)],
            "W": [(-1, 0), (-1, 1), (-1, -1)],
            "N": [(0, -1), (1, -1), (-1, -1)],
        }
        self.around = [
            (1, 0),
            (1, 1),
            (1, -1),
            (0, 1),
            (-1, 1),
            (-1, -1),
            (-1, 0),
            (0, -1),
        ]

    def reset(self):
        self.positions = self.getPositions(self.map)
        self.directions = ["N", "S", "W", "E"]

    def getPositions(self, plantMap: List[str]) -> List[List[int]]:
        positions = set()
        for y, row in enumerate(plantMap):
            for x, val in enumerate(row):
                if val == "#":
                    positions.add(f"{x},{y}")
        return positions

    def updateElves(self, pos: Set[str]) -> None:
        noChange = set()
        nextPos = {}
        hasNewPos = False
        
        # first half
        for coords in pos:
            x, y = map(int, coords.split(","))

            if all(f"{x+dx},{y+dy}" not in pos for dx, dy in self.around):
                noChange.add(f"{x},{y}")
                continue

            for direction in self.directions:
                checkDirs = self.dirMap[direction]
                isNewPos = not any(f"{x+dx},{y+dy}" in pos for dx, dy in checkDirs)

                if isNewPos:
                    newX, newY = x + checkDirs[0][0], y + checkDirs[0][1]

                    newKey = f"{newX},{newY}"
                    if newKey not in nextPos:
                        nextPos[f"{newX},{newY}"] = (x, y)
                    else:  # duplicate position, no need to update
                        if not nextPos[f"{newX},{newY}"]:
                            continue
                        prevX, prevY = nextPos[f"{newX},{newY}"]
                        noChange.add(f"{x},{y}")
                        noChange.add(f"{prevX},{prevY}")
                        nextPos[f"{newX},{newY}"] = None
                    break

            if not isNewPos:
                noChange.add(f"{x},{y}")

        # 2nd half
        for key, value in nextPos.items():
            if not value:
                continue
            x, y = map(int, key.split(","))
            if not hasNewPos:
                hasNewPos = True
            noChange.add(f"{x},{y}")

        self.directions.append(self.directions.pop(0))
        return [noChange, hasNewPos]

    def moveElves(self, rounds: int):
        self.reset()
        for _ in range(rounds):
            self.positions = self.updateElves(self.positions)[0]

        [maxX, maxY, minX, minY] = self.getMaxDimensions()
        width = maxX - minX + 1
        length = maxY - minY + 1
        return width * length - len(self.positions)

    def getFinishRounds(self):
        self.reset()
        hasNewPos = True
        rounds = 0
        while hasNewPos:
            self.positions, hasNewPos = self.updateElves(self.positions)
            rounds += 1
        return rounds

    def getMaxDimensions(self) -> List[int]:
        maxX = maxY = minX = minY = 0
        for coords in self.positions:
            x, y = map(int, coords.split(","))
            maxX = max(x, maxX)
            maxY = max(y, maxY)
            minX = min(x, minX)
            minY = min(y, minY)
        return [maxX, maxY, minX, minY]

    # For debugging
    def printPosition(self):
        maxX, maxY, minX, minY = self.getMaxDimensions()
        width = maxX - minX + 1
        length = maxY - minY + 1
        dataMap = [["." for _ in range(width)] for _ in range(length)]
        dataMap[-minY][-minX] = "O"
        for coords in self.positions:
            x, y = map(int, coords.split(","))
            dataMap[y - minY][x - minX] = "#"

        for row in dataMap:
            print(" ".join(row))


if __name__ == "__main__":
    elves = Elves(False)
    print("Day 23 part 1:", elves.moveElves(10))
    print("Day 23 part 2:", elves.getFinishRounds())
    #  Total Runtime ~6.6 s
