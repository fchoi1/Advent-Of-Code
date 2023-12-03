from typing import List, Optional
import re


class Checksum:
    def getInput(self) -> List[List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1:
                data.append([int(x) for x in line.split()])
        return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.numLists = self.getInput()

    def getChecksumTotal(self) -> int:
        return sum([max(n) - min(n) for n in self.numLists])

    def getCheckSumDivisible(self) -> int:
        total = 0
        for numList in self.numLists:
            numList.sort()
            found = False
            for i in range(len(numList)):
                if found:
                    break
                for j in range(i + 1, len(numList)):
                    if numList[j] % numList[i] == 0:
                        found = True
                        total += numList[j] // numList[i]
                        break
        return total


if __name__ == "__main__":
    checksum = Checksum()
    print("Day 2 part 1:", checksum.getChecksumTotal())
    print("Day 2 part 2:", checksum.getCheckSumDivisible())
