from typing import Optional, List, Set


class Rocks:
    def getInput(self) -> str:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
        return Lines[0].strip()

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.windData = self.getInput()

        self.chamberWidth = 7
        self.windLength = len(self.windData)
        self.fullReset()

        self.rocks = [
            [["#", "#", "#", "#"]],
            [
                [".", "#", "."],
                ["#", "#", "#"],
                [".", "#", "."],
            ],
            [
                ["#", "#", "#"],
                [".", ".", "#"],
                [".", ".", "#"],
            ],
            [["#"], ["#"], ["#"], ["#"]],
            [["#", "#"], ["#", "#"]],
        ]

    def fullReset(self) -> None:
        self.chamber = [["."] * self.chamberWidth]
        self.chamberHeights = [0] * self.chamberWidth
        self.highest = 0
        self.wind = 0
        self.cycleHeight = None
        self.cycleLength = None
        self.seen = {}

    def isOverlap(self, coords: List[int], rockType: int) -> bool:
        width = len(self.rocks[rockType][0])
        height = len(self.rocks[rockType])
        x, y = coords
        if x < 0 or x + width > len(self.chamber[0]) or y < 0:
            return True

        for i in range(width):
            for j in range(height):
                if (
                    self.chamber[y + j][x + i] == "#"
                    and self.rocks[rockType][j][i] == "#"
                ):
                    return True
        return False

    def dropPiece(self, rockNum: int) -> None:
        height = len(self.rocks[rockNum])

        startHeight = self.highest + 3
        coords = [2, startHeight]

        rows_to_add = max(0, startHeight + height - len(self.chamber) + 1)
        self.chamber.extend(["."] * self.chamberWidth for _ in range(rows_to_add))

        # Acutal Drop Piece Logic
        while not self.isOverlap(coords, rockNum):
            moveHorizontal = (
                -1 if self.windData[self.wind % self.windLength] == "<" else 1
            )
            if not self.isOverlap([coords[0] + moveHorizontal, coords[1]], rockNum):
                coords[0] += moveHorizontal

            coords[1] -= 1
            self.wind += 1

        coords[1] += 1
        self.updateChamber(coords, rockNum)
        self.highest = max(self.chamberHeights)

    def updateChamber(self, coords: List[int], rockNum: int) -> None:
        x, y = coords
        height = len(self.rocks[rockNum])
        width = len(self.rocks[rockNum][0])
        for i in range(width):
            for j in range(height):
                if self.rocks[rockNum][j][i] == "#":
                    self.chamber[y + j][x + i] = "#"
                    self.chamberHeights[x + i] = max(
                        self.chamberHeights[x + i], y + j + 1
                    )

    def getRockHeight(self, numRocks: int) -> int:
        self.fullReset()
        cycleExists = False

        for i in range(numRocks):
            currRock = i % len(self.rocks)
            self.dropPiece(currRock)
            if self.cycleFound(i, currRock, (self.wind - 1) % self.windLength):
                cycleExists = True
                break

        if not cycleExists:
            return self.highest

        fullCycles = (numRocks - i) // self.cycleLength
        heightAdd = fullCycles * self.cycleHeight
        remain = (numRocks - i) % self.cycleLength - 1
        nextRock = (i + 1) % len(self.rocks)

        for j in range(nextRock, nextRock + remain):
            currRock = j % len(self.rocks)
            self.dropPiece(currRock)

        return self.highest + heightAdd

    def cycleFound(self, rockCount: int, rockNum: int, wind: int) -> bool:
        # 18 rows is the number of rows to check for cycle
        currState = self.getState(self.chamber[self.highest - 18 : self.highest])

        key = f"{rockNum},{wind}"
        if key in self.seen:
            state = self.seen[key]["state"]
            height = self.seen[key]["height"]
            prevRockCount = self.seen[key]["rockCount"]

            if state == currState:
                self.cycleHeight = self.highest - height
                self.cycleLength = rockCount - prevRockCount
                return True

        self.seen[key] = {}
        self.seen[key]["state"] = currState
        self.seen[key]["height"] = self.highest
        self.seen[key]["rockCount"] = rockCount
        return False

    # Convertting row data to binary state representation
    def getState(self, rows: List[str]):
        return [
            [int("".join(row).replace("#", "1").replace(".", "0"), 2) for row in rows]
        ]

    # Used for debugging and visualization
    def printChamber(self, start: Optional[int] = None, end: Optional[int] = None):
        if not start or not end:
            start = 0
            end = len(self.chamber)
        for i, row in enumerate(reversed(self.chamber[start:end])):
            print(len(self.chamber) - i, "".join(row))
        print()


if __name__ == "__main__":
    rocks = Rocks()
    print("Day 17 part 1:", rocks.getRockHeight(2022))
    print("Day 17 part 2:", rocks.getRockHeight(1000000000000))
