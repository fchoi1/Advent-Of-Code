from typing import List, Optional, Set
import re


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
        print(len(self.map), len(self.map[0]))

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

        print(self.positions, len(self.positions))

    def getPositions(self, plantMap: List[str]) -> List[List[int]]:
        positions = set()
        for y, row in enumerate(plantMap):
            for x, val in enumerate(row):
                if val == "#":
                    positions.add(f"{x},{y}")
        return positions

    def moveElves(self, rounds: int):
        self.printPosition(self.getMaxDimensions())
        
        print(self.directions)
        for _ in range(rounds):
            print()
            noChange = set()
            nextPos = {}
            # first half
            for coords in self.positions:
                x, y = map(int, coords.split(","))

                if all(f"{x+dx},{y+dy}" in self.positions for dx, dy in self.around):
                    noChange.add(f"{x},{y}")
                    continue

                # check all around  first
                newX = newY = None

                for direction in self.directions:
                    checkDirs = self.dirMap[direction]

                    isNewPos = not any(
                        f"{x+dx},{y+dy}" in self.positions for dx, dy in checkDirs
                    )
                    if isNewPos:
                        newX = x + checkDirs[0][0]
                        newY = y + checkDirs[0][1]

                        print('old', x, y, 'new pos', newX, newY, 'checkDirs', direction)

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
                noChange.add(f"{x},{y}")

            self.directions.append(self.directions.pop(0))
            self.positions = noChange
            
            print(self.getMaxDimensions())

            self.printPosition(self.getMaxDimensions())

        [maxX, maxY, minX, minY] = self.getMaxDimensions()
        width = maxX - minX + 1
        length = maxY - minY + 1
        return (width*length - len(self.positions))

    def getMaxDimensions(self) -> List[int]:
        maxX = maxY = minX = minY = 0

        for coords in self.positions:
            x, y = map(int, coords.split(","))
            maxX = max(x, maxX)
            maxY = max(y, maxY)
            minX = min(x, minX)
            minY = min(y, minY)
        return [maxX, maxY, minX, minY]

    def printPosition(self, dimensions: List[int]):
        maxX, maxY, minX, minY = dimensions
        width = maxX - minX + 1
        length = maxY - minY + 1
        dataMap = [["." for _ in range(width)] for _ in range(length)]
        for coords in self.positions:
            x, y = map(int, coords.split(","))
            dataMap[y - minY][x - minX] = "#"

        for row in dataMap:
            print(" ".join(row))

        pass


if __name__ == "__main__":
    elves = Elves(True)
    print("Day 23 part 1:", elves.moveElves(2))
    print("Day 23 part 2:")
