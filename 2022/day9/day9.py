from typing import List, Optional


class Rope:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x.strip().split() for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.inputData = self.getInput()
        self.visitedOnceSingle = 1
        self.visitedOnceLast = 1
        self.visitedSingle = set()
        self.visitedLast = set()
        self.head = [0, 0]
        self.tails = []
        self.createTails(9)

    def createTails(self, number: int) -> None:
        for _ in range(number):
            self.tails.append([0, 0])

    def tailInRange(self, h: List[int], t: List[int]) -> bool:
        return h[0] - 1 <= t[0] <= h[0] + 1 and h[1] - 1 <= t[1] <= h[1] + 1

    def moveHead(self, direction: str, steps: int) -> None:
        dirSteps = {"R": [1, 0], "L": [-1, 0], "U": [0, 1], "D": [0, -1]}
        for i in range(steps):
            self.head[0] = self.head[0] + dirSteps[direction][0]
            self.head[1] = self.head[1] + dirSteps[direction][1]

            for i in range(len(self.tails)):
                currHead = self.head if i == 0 else self.tails[i - 1]

                if self.tailInRange(currHead, self.tails[i]):
                    break

                rowValue = currHead[0] - self.tails[i][0]
                colValue = currHead[1] - self.tails[i][1]
                if rowValue != 0:
                    rowValue /= abs(rowValue)
                if colValue != 0:
                    colValue /= abs(colValue)
                self.tails[i][0] += rowValue
                self.tails[i][1] += colValue

            lastTail = self.tails[len(self.tails) - 1]
            singleTail = self.tails[0]
            self.visitedLast.add(tuple(lastTail))
            self.visitedSingle.add(tuple(singleTail))

    def getUniqueSingleTail(self) -> int:
        self.moveRope()
        return len(self.visitedSingle)

    def getUniqueLastTail(self) -> int:
        return len(self.visitedLast)

    def moveRope(self) -> None:
        for direction, steps in self.inputData:
            self.moveHead(direction, int(steps))


if __name__ == "__main__":
    rope = Rope()
    print("Day 9 part 1:", rope.getUniqueSingleTail())
    print("Day 9 part 2:", rope.getUniqueLastTail())
