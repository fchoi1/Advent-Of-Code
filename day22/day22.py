from typing import List, Optional
import re


class MonkeyMap:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        delimiters = [""]
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                line = line.replace("\n", "")
                line = re.split("|".join(map(re.escape, delimiters)), line)[1:-1]
                data.append(line)
            return [data[:-2], "".join(data[len(data) - 1])]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        """Main entry point of the app"""
        self.useTest = useTest
        self.map, self.directions = self.getInput()
        self.map = self.fillEmpty(self.map)

        self.directions = self.parseDirections(self.directions)
        self.start = self.getStart()

        self.dirCycle = ["R", "D", "L", "U"]
        self.dirMap = {"R": [1, 0], "D": [0, 1], "L": [-1, 0], "U": [0, -1]}
        self.dirIndex = 0

    def getStart(self) -> None | List[int]:
        for i, val in enumerate(self.map[0]):
            if val == ".":
                return [i, 0]
        return None

    def fillEmpty(self, dataMap: List[str]) -> List[str]:
        length = len(max(dataMap, key=len))
        for row in dataMap:
            if len(row) < length:
                empty = [" "] * (length - len(row))
                row.extend(empty)
        return dataMap

    def parseDirections(self, dirString: str) -> List[str | int]:
        directions = []
        numStr = ""
        for val in dirString:
            if val.isupper():
                directions.append(int(numStr))
                directions.append(val)
                numStr = ""
                continue
            numStr += val
        directions.append(int(numStr))
        return directions

    def getPassword(self, isCube: Optional[bool] = False) -> int:
        currDir = "R"
        currCoord = self.start
        self.dirIndex = 0

        for direction in self.directions[:]:
            if isinstance(direction, int):
                currDir = self.dirCycle[self.dirIndex % 4]
                for _ in range(direction):
                    dx, dy = self.dirMap[currDir]
                    if self.isOutofBounds([currCoord[0] + dx, currCoord[1] + dy]):
                        [tempx, tempy, tempDir] = (
                            self.getCubeWrapCoords(currCoord, currDir)
                            if isCube
                            else self.getDefaultWrapCoords(currCoord, currDir)
                        )

                        if self.map[tempy][tempx] == "#":
                            break

                        currCoord = [tempx, tempy]
                        currDir = tempDir
                        self.dirIndex = self.dirCycle.index(currDir)

                    else:
                        currCoord[0] += dx
                        currCoord[1] += dy

                        if self.map[currCoord[1]][currCoord[0]] == "#":
                            currCoord[0] -= dx
                            currCoord[1] -= dy
                            break
                continue
            self.dirIndex += 1 if direction == "R" else -1

        return 1000 * (currCoord[1] + 1) + 4 * (currCoord[0] + 1) + (self.dirIndex % 4)

    def isOutofBounds(self, coords: List[int]) -> bool:
        x, y = coords
        if not (0 <= y < len(self.map)) or not (0 <= x < len(self.map[y])):
            return True
        return self.map[y][x] == " "

    def getDefaultWrapCoords(self, coords: List[int], currDir: str) -> List[int]:
        x, y = coords
        x_direction = -1 if currDir == "R" else 1 if currDir == "L" else 0
        y_direction = 1 if currDir == "U" else -1 if currDir == "D" else 0

        while (
            0 <= y < len(self.map)
            and 0 <= x < len(self.map[y])
            and self.map[y][x] != " "
        ):
            x += x_direction
            y += y_direction

        return [x - x_direction, y - y_direction, currDir]

    # hardCode part 2 (T T)
    def getCubeWrapCoords(self, coords: List[int], currDir: str) -> List[int | str]:
        x, y = coords
        zone = self.getFace(coords)
        if zone == 1:
            if currDir == "U":
                # Zone 6 going up
                return [x - 100, 199, "U"]
            elif currDir == "R":
                #  zone 4 going left
                return [99, 149 - y, "L"]
            elif currDir == "D":
                #  zone 3 going left (rotate)
                return [99, x - 50, "L"]

        elif zone == 2:
            if currDir == "U":
                # zone 6 going right (rotate)
                return [0, x + 100, "R"]

            elif currDir == "L":
                # zone 5 going right
                return [0, 149 - y, "R"]

        elif zone == 3:
            if currDir == "R":
                # zone 1 going up (rotate)
                return [y + 50, 49, "U"]
            elif currDir == "L":
                # zone 5  going  down
                return [y - 50, 100, "D"]

        elif zone == 4:
            if currDir == "R":
                # zone 1 going Left
                return [149, 149 - y, "L"]
            elif currDir == "D":
                # zone 6  going left (Rotate)
                return [49, x + 100, "L"]

        elif zone == 5:
            if currDir == "L":
                # zone 2 going right
                return [50, 149 - y, "R"]
            elif currDir == "U":
                # zone 3 going right (Rotate)
                return [50, x + 50, "R"]

        elif zone == 6:
            if currDir == "L":
                # zone 2 going down (Rotate)
                return [y - 100, 0, "D"]
            elif currDir == "R":
                # zone 4 going up (rotate)
                return [y - 100, 149, "U"]
            elif currDir == "D":
                # zone 1 going down
                return [x + 100, 0, "D"]

        return [coords[0], coords[1], currDir]

    def getFace(self, coords: List[int]) -> int:
        x, y = coords
        if 100 <= x < 150 and 0 <= y < 50:
            return 1
        elif 50 <= x < 100 and 0 <= y < 50:
            return 2
        elif 50 <= x < 100 and 50 <= y < 100:
            return 3
        elif 50 <= x < 100 and 100 <= y < 150:
            return 4
        elif 0 <= x < 50 and 100 <= y < 150:
            return 5
        elif 0 <= x < 50 and 150 <= y < 200:
            return 6
        return 0


if __name__ == "__main__":
    """This is executed when run from the command line"""
    monkeyMap = MonkeyMap(False)
    print("Day 22 part 1:", monkeyMap.getPassword(False))
    print("Day 22 part 2:", monkeyMap.getPassword(True))
