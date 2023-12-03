from typing import List, Optional


class Boarding:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x.strip() for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.passes = self.getInput()
        self.highest = 0
        self.seatId = set()

    def getHighestSeat(self) -> int:
        for boardingPass in self.passes:
            seatId = self.getRow(boardingPass) * 8 + self.getSeat(boardingPass)
            self.seatId.add(seatId)
            self.highest = max(self.highest, seatId)
        return self.highest

    def getYourSeat(self) -> int:
        count = self.highest
        while count > 0:
            count -= 1
            if count not in self.seatId:
                return count
        return -1

    def getRow(self, boardingPass: str) -> int:
        return self.binarySearch(boardingPass[:7], 0, 127, "F")

    def getSeat(self, boardingPass: str) -> int:
        return self.binarySearch(boardingPass[7:], 0, 7, "L")

    def binarySearch(self, code: str, start: int, end: int, dir: str) -> int:
        for char in code:
            mid = (start + end) // 2
            if char == dir:
                end = mid
            else:
                start = mid + 1
        return start


if __name__ == "__main__":
    boarding = Boarding()
    print("Day 5 part 1:", boarding.getHighestSeat())
    print("Day 5 part 2:", boarding.getYourSeat())
