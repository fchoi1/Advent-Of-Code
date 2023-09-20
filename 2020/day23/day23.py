from typing import Optional, List, Dict


class Cups:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(x) for x in file1.readline()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.cups = self.getInput()
        self.min = min(self.cups)
        self.max = max(self.cups)
        self.cupDict = self.getNumDict(self.cups)

    def getNumDict(self, numList: int) -> Dict:
        return {numList[i]: numList[(i + 1) % len(numList)] for i in range(len(numList))}

    def moveCups(self, currentVal: int) -> int:
        nextVal = currentVal
        removed = []
        for _ in range(3):
            nextVal = self.cupDict[nextVal]
            removed.append(nextVal)

        nextVal = self.cupDict[nextVal]
        self.cupDict[currentVal] = nextVal

        target = currentVal - 1
        while target in removed or target < self.min:
            if target < self.min:
                target = self.max
            else:
                target -= 1

        temp = self.cupDict[target]
        self.cupDict[target] = removed[0]
        self.cupDict[removed[2]] = temp

        return nextVal

    def fillCups(self):
        val = self.max
        while val < 1000000:
            val += 1
            self.cups.append(val)
        self.max = val
        self.cupDict = self.getNumDict(self.cups)

    def getOrder(self) -> str:
        self.cupDict = self.getNumDict(self.cups)
        nextVal = self.cups[0]
        for _ in range(100):
            nextVal = self.moveCups(nextVal)

        nextVal = 1
        result = []
        for _ in range(len(self.cupDict) - 1):
            result.append(str(self.cupDict[nextVal]))
            nextVal = self.cupDict[nextVal]
        return "".join(result)

    def getOrder2(self) -> str:
        self.fillCups()
        nextVal = self.cups[0]
        for _ in range(10_000_000):
            nextVal = self.moveCups(nextVal)
        return self.cupDict[1] * self.cupDict[self.cupDict[1]]


if __name__ == "__main__":
    cups = Cups()
    print("Day 23 part 1:", cups.getOrder())
    print("Day 23 part 2:", cups.getOrder2())
    # Total Runtime ~8.2s