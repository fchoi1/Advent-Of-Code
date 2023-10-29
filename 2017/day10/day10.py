from typing import List, Optional


class Knot:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(x) for x in file1.readline().strip().split(",")]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.lengths = self.getInput()
        self.length = 5 if useTest else 256
        self.hash = [i for i in range(self.length)]
        self.firstTwo = 0
        self.runLengths()

    def reverseSubset(self, start: int, end: int):
        if end > self.length:
            end %= self.length
            sublist = list(reversed(self.hash[start:] + self.hash[:end]))
            self.hash[start:] = sublist[: len(self.hash) - start]
            self.hash[:end] = sublist[len(self.hash) - start :]
        else:
            self.hash[start:end] = reversed(self.hash[start:end])

    def runLengths(self) -> None:
        skip = index = 0
        for l in self.lengths:
            subset = index + l
            self.reverseSubset(index, subset)
            index = (subset + skip) % self.length
            skip += 1
        self.firstTwo = self.hash[0] * self.hash[1]

    def getFirstTwo(self) -> int:
        return self.firstTwo


if __name__ == "__main__":
    knot = Knot()
    print("Day 10 part 1:", knot.getFirstTwo())
    # print("Day 10 part 2:", knot.getGarbage())
