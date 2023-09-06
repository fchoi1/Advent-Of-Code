import ast
from typing import List, Optional


class Signal:
    def getInput1(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
            data = []
            dataPair = []
            for line in Lines:
                if not line.strip():
                    data.append(dataPair)
                    dataPair = []
                    continue
                my_list = ast.literal_eval(line.strip())
                dataPair.append(my_list)
            data.append(dataPair)
            return data

    def getInput2(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
            data = []
            for line in Lines:
                if line.strip():
                    data.append(ast.literal_eval(line.strip()))
            return data

    def compareList(self, left: List, right: List) -> bool:
        rightLength = len(right)
        leftLength = len(left)

        if not left and not right:
            return None

        for i in range(len(left)):
            if i >= rightLength:
                return False
            if isinstance(left[i], int) and isinstance(right[i], int):
                if left[i] < right[i]:
                    return True
                elif left[i] > right[i]:
                    return False
                continue

            leftTemp = [left[i]] if isinstance(left[i], int) else left[i]
            rightTemp = [right[i]] if isinstance(right[i], int) else right[i]

            listResult = self.compareList(leftTemp, rightTemp)
            if listResult is not None:
                return listResult

        if rightLength > leftLength:
            return True

        return None

    def evaluateSignals(self) -> None:
        for i, [leftSignal, rightSignal] in enumerate(self.inputData1):
            if self.compareList(leftSignal, rightSignal):
                self.correctIndices.append(i + 1)

    def compareValue(self, signal: List) -> None:
        if not signal:
            self.before2 += 1
            return
        if isinstance(signal[0], int):
            if signal[0] < self.firstPacket:
                self.before2 += 1

            elif self.firstPacket <= signal[0] < self.secondPacket:
                self.between += 1
            return
        self.compareValue(signal[0])

    def getDecorder(self) -> int:
        for signal in self.inputData2:
            self.compareValue(signal)
        return self.before2 * (self.before2 + self.between)

    def getSumofCorrectIdices(self) -> int:
        return sum(self.correctIndices)

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.inputData1 = self.getInput1()
        self.inputData2 = self.getInput2()

        self.firstPacket = 2
        self.secondPacket = 6
        self.before2 = 1
        self.between = 1
        self.correctIndices = []


if __name__ == "__main__":
    signal = Signal()
    signal.evaluateSignals()
    print("Day 13 part 1:", signal.getSumofCorrectIdices())
    print("Day 13 part 2:", signal.getDecorder())
