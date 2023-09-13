from typing import Optional, List
import math


class Ferry:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                data.append((line.strip()[0], int(line.strip()[1:])))
        return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.commands = self.getInput()
        self.currDir = 0
        self.dir = "ESWN"
        self.dirMap = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        self.reset()

    def reset(self) -> None:
        self.pos = [0, 0]
        self.waypoint = [10, 1]

    def moveShip(self) -> None:
        self.reset()
        for command, val in self.commands:
            if command in "RL":
                shift = val // 90 if command == "R" else -val // 90
                self.currDir = (self.currDir + shift) % 4
                continue

            elif command == "F":
                index = self.currDir

            elif command in "ESWN":
                index = self.dir.index(command)

            dx, dy = self.dirMap[index]
            self.pos = [self.pos[0] + dx * val, self.pos[1] + dy * val]

    def moveShip2(self) -> None:
        self.reset()
        for command, val in self.commands:
            # invert Waypoint, rotation matrix
            if command in "RL":
                degree = math.radians(-val) if command == "R" else math.radians(val)
                cos_theta = int(math.cos(degree))
                sin_theta = int(math.sin(degree))

                self.waypoint[0], self.waypoint[1] = (
                    cos_theta * self.waypoint[0] - sin_theta * self.waypoint[1],
                    sin_theta * self.waypoint[0] + cos_theta * self.waypoint[1],
                )
                continue

            elif command == "F":
                dx, dy = self.waypoint
                self.pos = [self.pos[0] + dx * val, self.pos[1] + dy * val]

            elif command in "ESWN":
                index = self.dir.index(command)
                dx, dy = self.dirMap[index]
                self.waypoint = [self.waypoint[0] + dx * val, self.waypoint[1] + dy * val]

    def getDistance(self) -> int:
        self.moveShip()
        return abs(self.pos[0]) + abs(self.pos[1])

    def getDistance2(self) -> int:
        self.moveShip2()
        return abs(self.pos[0]) + abs(self.pos[1])


if __name__ == "__main__":
    ferry = Ferry()
    print("Day 12 part 1:", ferry.getDistance())
    print("Day 12 part 2:", ferry.getDistance2())
