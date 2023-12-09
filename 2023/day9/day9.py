from typing import List, Optional


class Mirage:
    def getInput(self) -> List[List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [[int(x) for x in line.strip().split()] for line in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.histories = self.getInput()
        self.firstSum, self.lastSum = 0, 0
        self.scan()

    def scan(self) -> None:
        for history in self.histories:
            diffs = [history]
            while any(history):
                history = [n - prev for prev, n in zip(history, history[1:])]
                diffs.append(history)
            last, first = 0, 0
            for diff in reversed(diffs):
                last, first = last + diff[-1], diff[0] - first
            self.lastSum += last
            self.firstSum += first

    def getLastSum(self) -> int:
        return self.lastSum

    def getFirstSum(self) -> int:
        return self.firstSum


if __name__ == "__main__":
    mirage = Mirage()
    print("Day 9 part 1:", mirage.getLastSum())
    print("Day 9 part 2:", mirage.getFirstSum())
