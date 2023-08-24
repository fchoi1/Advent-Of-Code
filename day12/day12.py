from typing import Tuple, List, Optional


class Hill:
    def getInput(self) -> List[List[str]]:
        with open("input.txt", "r") as file1:
            # with open('input-test.txt', 'r') as file1:
            Lines = file1.readlines()
            return [list(line.strip()) for line in Lines]

    def getStart(self) -> Tuple[int, int]:
        return next(
            (
                (x, y)
                for y, row in enumerate(self.inputData)
                for x, value in enumerate(row)
                if value == "S"
            ),
            (-1, -1),
        )

    def getEnd(self) -> Tuple[int, int]:
        return next(
            (
                (x, y)
                for y, row in enumerate(self.inputData)
                for x, value in enumerate(row)
                if value == "E"
            ),
            (-1, -1),
        )

    def solve(self, goal: str, useStart: Optional[bool] = True) -> int:
        self.reset()
        startLocation = self.start if useStart else self.end
        self.q.append(startLocation)
        self.visited[startLocation] = True

        while self.q:
            nextQ = []
            tempQ = self.q
            for currentX, currentY in tempQ:
                elevation = self.inputData[currentY][currentX]
                if elevation == goal:
                    return self.step

                elevation = "a" if elevation == "S" else elevation
                elevation = "z" if elevation == "E" else elevation

                nextQ = self.checkAllowPath(
                    (currentX, currentY), elevation, nextQ, useStart
                )
            self.q = nextQ
            self.step += 1
        return -1

    def checkAllowPath(
        self, current: Tuple, elevation: str, nextQ: List, fromStart
    ) -> List[Tuple[int, int]]:
        (currentX, currentY) = current
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        elevation_mapping = {"E": "z", "S": "a"}

        for y, x in directions:
            temp = (currentX + x, currentY + y)
            if (
                not (0 <= temp[1] < self.length)
                or not (0 <= temp[0] < self.width)
                or (temp in self.visited)
            ):
                continue

            tempElevation = self.inputData[temp[1]][temp[0]]
            tempElevation = elevation_mapping.get(tempElevation, tempElevation)

            if fromStart and ord(tempElevation) <= ord(elevation) + 1:
                nextQ.append(temp)
                self.visited[temp] = True
            elif not fromStart and ord(tempElevation) >= ord(elevation) - 1:
                nextQ.append(temp)
                self.visited[temp] = True
        return nextQ

    def reset(self) -> None:
        self.visited = {}
        self.step = 0
        self.q = []

    def __init__(self) -> None:
        """Main entry point of the app"""
        self.inputData = self.getInput()
        self.start = self.getStart()
        self.end = self.getEnd()
        self.length = len(self.inputData)  #  Y
        self.width = len(self.inputData[0])  # X
        self.step = 0
        self.visited = {}
        self.q = []


if __name__ == "__main__":
    """This is executed when run from the command line"""
    hill = Hill()
    print("Day 12 part 1:", hill.solve("E"))
    print("Day 12 part 2:", hill.solve("a", False))
