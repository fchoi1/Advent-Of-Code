from typing import List, Optional


class Rope:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x.strip() for x in file1]

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
        for i in range(number):
            self.tails.append([0, 0])

    def tailInRange(self, head: List[int], tail: List[int]) -> bool:
        return head[0] - 1 <= tail[0] <= head[0] + 1 and head[1] - 1 <= tail[1] <= head[1] + 1

    def tailInRow(self, head: List[int], tail: List[int]) -> int:
        return head[0] - tail[0]

    def tailInCol(self, head: List[int], tail: List[int]) -> int:
        return head[1] - tail[1]

    def moveHead(self, direction: str, steps: int) -> None:
        dirSteps = {"R": [1, 0], "L": [-1, 0], "U": [0, 1], "D": [0, -1]}
        for i in range(steps):
            self.head[0] = self.head[0] + dirSteps[direction][0]
            self.head[1] = self.head[1] + dirSteps[direction][1]

            for i in range(len(self.tails)):
                if i == 0:
                    currHead = self.head
                else:
                    currHead = self.tails[i - 1]

                if self.tailInRange(currHead, self.tails[i]):
                    break

                rowValue = self.tailInRow(currHead, self.tails[i])
                colValue = self.tailInCol(currHead, self.tails[i])
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
        for instruction in self.inputData:
            [direction, steps] = [
                instruction.split(" ")[0],
                int(instruction.split(" ")[1]),
            ]
            self.moveHead(direction, steps)


if __name__ == "__main__":
    """This isexecuted when run from the command line"""
    rope = Rope()
    print("Day 9 part 1:", rope.getUniqueSingleTail())
    print("Day 9 part 2:", rope.getUniqueLastTail())
