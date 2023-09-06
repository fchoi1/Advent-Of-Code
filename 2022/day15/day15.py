from typing import List, Optional, Tuple
import re


class Beacon:
    def getInput(self) -> List[List[Tuple[int]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
            data = []
            delimiters = ["Sensor at x=", ", y=", ": closest beacon is at x="]
            for line in Lines:
                coords = list(
                    map(
                        int,
                        re.split("|".join(map(re.escape, delimiters)), line.strip())[
                            1:
                        ],
                    )
                )
                data.append([(coords[0], coords[1]), (coords[2], coords[3])])
            return data

    def checkPair(self, sensorY: int, distance: int, row: int) -> bool:
        return (sensorY >= row and sensorY - distance <= row) or (
            sensorY < row and sensorY + distance >= row
        )

    def merge_intervals(
        self, intervals: List[List[int]], new_interval: List[int]
    ) -> List[List[int]]:
        i = 0
        while i < len(intervals) and intervals[i][1] < new_interval[0]:
            i += 1
        while i < len(intervals) and intervals[i][0] <= new_interval[1]:
            new_interval = [
                min(new_interval[0], intervals[i][0]),
                max(new_interval[1], intervals[i][1]),
            ]
            intervals.pop(i)
        intervals.insert(i, new_interval)
        return intervals

    def checkSensors(
        self, useLimits: bool = False, minX: int = 0, maxX: int = 0, row: int = -1
    ) -> None:
        for [(sX, sY), (bX, bY)] in self.inputData[:]:
            distance = abs(bX - sX) + abs(bY - sY)
            if not useLimits:
                row = self.row
            if self.checkPair(sY, distance, row):
                yDiff = abs(row - sY)
                xDiff = distance - yDiff
                xRange = [sX - xDiff, sX + xDiff]
                if useLimits:
                    if xRange[0] < minX:
                        xRange[0] = minX
                    if xRange[1] > maxX:
                        xRange[1] = maxX
                self.BeaconRanges = self.merge_intervals(self.BeaconRanges, xRange)

    def findSingleBeacon(self, x: int = 20, y: int = 20) -> int:
        for i in range(y):
            self.BeaconRanges = []
            self.checkSensors(True, 0, x, i)

            if len(self.BeaconRanges) > 1:
                break
        hiddenBeacon = [self.BeaconRanges[0][1] + 1, i]
        return hiddenBeacon[0] * 4_000_000 + hiddenBeacon[1]

    def getEmptySpots(self) -> int:
        self.BeaconRanges = []
        self.checkSensors()
        count = 0
        for [x1, x2] in self.BeaconRanges:
            count += x2 - x1
        return count

    def __init__(self, row: int = 10, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.inputData = self.getInput()
        self.BeaconRanges = []
        self.row = 10 if useTest else row


if __name__ == "__main__":
    beacon = Beacon(2_000_000)
    print("Day 15 part 1:", beacon.getEmptySpots())
    print("Day 15 part 2:", beacon.findSingleBeacon(4_000_000, 4_000_000))
    # Runtime ~37 seconds
