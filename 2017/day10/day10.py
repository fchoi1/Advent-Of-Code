import os
from typing import List, Optional
from functools import reduce


class Knot:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        scriptDir = os.path.dirname(
            os.path.abspath(__file__)
        )  # need absolute path for day 14
        filePath = os.path.join(scriptDir, inputFile)
        with open(filePath, "r") as file1:
            return [int(x) for x in file1.readline().strip().split(",")]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.lengths = self.getInput()
        self.length = 256
        self.firstTwo = 0

    def reset(self, isPart2: Optional[bool] = False) -> None:
        length = 5 if self.useTest and not isPart2 else 256
        self.hash = [i for i in range(length)]
        self.skip = self.index = 0

    def getNewLengths(self, string: str) -> List[int]:
        lengths = [ord(char) for char in string]
        lengths += [17, 31, 73, 47, 23]
        return lengths

    def reverseSubset(self, start: int, end: int) -> None:
        if end > len(self.hash):
            end %= len(self.hash)
            sublist = list(reversed(self.hash[start:] + self.hash[:end]))
            self.hash[start:] = sublist[: len(self.hash) - start]
            self.hash[:end] = sublist[len(self.hash) - start :]
        else:
            self.hash[start:end] = reversed(self.hash[start:end])

    def runLengths(self, lengths: List[int]) -> None:
        for l in lengths:
            subset = self.index + l
            self.reverseSubset(self.index, subset)
            self.index = (subset + self.skip) % len(self.hash)
            self.skip += 1
        self.firstTwo = self.hash[0] * self.hash[1]

    def getFirstTwo(self) -> int:
        self.reset()
        self.runLengths(self.lengths)
        return self.firstTwo

    def densitfy(self, hashList: List[int]) -> int:
        return reduce(lambda x, y: x ^ y, hashList)

    def generateKnotHash(self, string: Optional[str] = "") -> str:
        self.reset(True)
        newLengths = (
            self.getNewLengths(string)
            if string
            else self.getNewLengths(",".join(map(str, self.lengths)))
        )
        stringHash = ""
        for _ in range(64):
            self.runLengths(newLengths)
        for i in range(self.length // 16):
            val = self.densitfy(self.hash[i * 16 : (i + 1) * 16])
            stringHash += format(val, "02x")
        return stringHash


if __name__ == "__main__":
    knot = Knot(True)
    print("Day 10 part 1:", knot.getFirstTwo())
    print("Day 10 part 2:", knot.generateKnotHash())
