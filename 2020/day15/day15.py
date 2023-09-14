from typing import Optional, List
from collections import deque


class Recitation:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(val) for val in file1.readlines()[0].split(",")]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.reset()

    def reset(self) -> None:
        self.cache = {}
        self.starting = deque(self.getInput())

    def getNumberSpoken(self, rounds: Optional[int] = 2020) -> int:
        self.reset()
        nextVal = self.starting.popleft()
        for i in range(1, rounds):
            if nextVal in self.cache:
                temp = nextVal
                nextVal = i - self.cache[nextVal]
                self.cache[temp] = i
            else:
                self.cache[nextVal] = i
                if self.starting:
                    self.cache[nextVal] = i
                    nextVal = self.starting.popleft()
                else:
                    nextVal = 0
        return nextVal


if __name__ == "__main__":
    recitation = Recitation()
    print("Day 15 part 1:", recitation.getNumberSpoken())
    print("Day 15 part 2:", recitation.getNumberSpoken(30000000))
    # Total Runtime ~7.5s
