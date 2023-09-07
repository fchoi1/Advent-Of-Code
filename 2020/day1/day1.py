from typing import List, Optional


class Report:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
            data = []
            for line in Lines:
                line = line.strip()
                data.append(int(line))
        return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.list = self.getInput()

    def getTwoEntries(self, numList: Optional[List | None] = None, target: Optional[int] = 2020) -> int:
        numDict = set()
        if not numList:
            numList = self.list
        for i in numList:
            diff = target - i
            if i in numDict:
                print(diff, i)
                return diff * i
            numDict.add(diff)
        return None

    def getThreeEntries(self, target: Optional[int] = 2020) -> int:
        for i, val in enumerate(self.list):
            tempTarget = target - val
            product = self.getTwoEntries(self.list[i:], tempTarget)
            if product:
                return product * val
        return None


if __name__ == "__main__":
    report = Report()
    print("Day 1 part 1:", report.getTwoEntries())
    print("Day 1 part 2:", report.getThreeEntries())
