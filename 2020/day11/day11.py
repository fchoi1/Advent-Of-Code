from typing import Optional, List, Tuple


class Seat:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                data.append(list(line.strip()))
        return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.seats = self.getInput()
        self.length = len(self.seats)
        self.width = len(self.seats[0])
        self.directions = [(0, 1), (1, 1), (-1, 1), (1, 0), (1, -1), (-1, -1), (0, -1), (-1, 0)]
        self.occupied = 0

    def shouldBeEmpty(self, pos: Tuple[int]) -> bool:
        x, y = pos
        count = 0
        for dx, dy in self.directions:
            if self.inBounds(x + dx, y + dy) and self.seats[y + dy][x + dx] == "#":
                count += 1
            if count >= 4:
                return True
        return False

    def shouldBeOccupied(self, pos: Tuple[int]) -> bool:
        x, y = pos
        for dx, dy in self.directions:
            if self.inBounds(x + dx, y + dy) and self.seats[y + dy][x + dx] == "#":
                return False
        return True

    def shouldBeOccupied2(self, pos: Tuple[int]) -> bool:
        for dx, dy in self.directions:
            x, y = pos
            while self.inBounds(x + dx, y + dy):
                if self.seats[y + dy][x + dx] == "L":
                    break

                elif self.seats[y + dy][x + dx] == "#":
                    return False
                x += dx
                y += dy
        return True

    def shouldBeEmpty2(self, pos: Tuple[int]) -> bool:
        count = 0
        for dx, dy in self.directions:
            x, y = pos
            while self.inBounds(x + dx, y + dy):
                if self.seats[y + dy][x + dx] == "L":
                    break

                elif self.seats[y + dy][x + dx] == "#":
                    count += 1
                    if count >= 5:
                        return True
                    break
                x += dx
                y += dy
        return False

    def inBounds(self, x, y) -> bool:
        return 0 <= x < self.width and 0 <= y < self.length

    def moveSeats(self, useNewRules: bool) -> int:
        shouldBeEmpty = self.shouldBeEmpty2 if useNewRules else self.shouldBeEmpty
        shouldBeOccupied = self.shouldBeOccupied2 if useNewRules else self.shouldBeOccupied
        newSeats = []
        hasSeatsChanged = False
        for y in range(self.length):
            seatRow = []
            for x in range(self.width):
                # print('curr', x, y, self.seats[y][x])
                if self.seats[y][x] == "#" and shouldBeEmpty((x, y)):
                    seatRow.append("L")
                    hasSeatsChanged = True
                elif self.seats[y][x] == "L" and shouldBeOccupied((x, y)):
                    seatRow.append("#")
                    hasSeatsChanged = True
                    self.occupied += 1
                else:
                    if self.seats[y][x] == "#":
                        self.occupied += 1
                    seatRow.append(self.seats[y][x])
            newSeats.append(seatRow)
        self.seats = newSeats
        return hasSeatsChanged

    def getOccupied(self, useNewRules: Optional[bool] = False) -> int:
        self.seats = self.getInput()
        hasSeatsChanged = True
        while hasSeatsChanged:
            self.occupied = 0
            hasSeatsChanged = self.moveSeats(useNewRules)
        return self.occupied


if __name__ == "__main__":
    seat = Seat()
    print("Day 11 part 1:", seat.getOccupied())
    print("Day 11 part 2:", seat.getOccupied(True))
