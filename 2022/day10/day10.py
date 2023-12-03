from typing import List, Optional


class Tube:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x.strip() for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.inputData = self.getInput()
        self.cycle = 0
        self.value = 1
        self.signalStrengths = [20, 60, 100, 140, 180, 220]
        self.totalSum = 0
        self.CRTrow = 6
        self.CRTpixel = 40
        self.CRT = [["."] * self.CRTpixel for i in range(self.CRTrow)]

    def runProgram(self) -> None:
        for row in self.inputData:
            commandArr = row.split(" ")
            self.updateCRT()
            self.cycle += 1
            self.checkSignalStrength()

            if commandArr[0] == "addx":
                self.updateCRT()
                self.cycle += 1
                self.checkSignalStrength()
                self.value += int(row.split(" ")[1])

    def checkSignalStrength(self) -> None:
        if self.cycle in self.signalStrengths:
            strength = self.signalStrengths.pop(self.signalStrengths.index(self.cycle))
            self.totalSum += self.value * strength

    def updateCRT(self) -> None:
        self.currRow = self.cycle // 40
        self.currCol = self.cycle % 40
        if self.value - 1 <= self.cycle % 40 <= self.value + 1:
            self.CRT[self.currRow][self.currCol] = "#"

    def getTotalSum(self) -> int:
        self.runProgram()
        return self.totalSum

    def printCRT(self) -> None:
        for row in self.CRT:
            print("  ".join(row))
        pass


if __name__ == "__main__":
    """This isexecuted when run from the command line"""
    tube = Tube()
    print("Day 10 part 1:", tube.getTotalSum())
    print("Day 10 part 2:", tube.printCRT())
