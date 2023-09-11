from typing import Optional, List, Tuple


class Encoding:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(line.strip()) for line in file1.readlines()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.length = 5 if self.useTest else 25
        self.input = self.getInput()

    def findError(self):
        for i in range(self.length, len(self.input)):
            if not self.inPreamble(self.input[i - self.length : i], self.input[i]):
                return self.input[i]
        return -1

    def inPreamble(self, preamble: List[int], target: int) -> bool:
        numDict = set()
        for i in preamble:
            if i in numDict:
                return True
            numDict.add(target - i)
        return False

    def getContiguous(self) -> Tuple[int]:
        target = self.findError()
        total = start = 0

        for i, val in enumerate(self.input):
            total += val

            while total > target:
                total -= self.input[start]
                start += 1

            if total == target:
                return (start, i)
        return (-1, -1)

    def getWeakness(self) -> int:
        start, end = self.getContiguous()
        array = self.input[start:end]
        return max(array) + min(array)


if __name__ == "__main__":
    encoding = Encoding()
    print("Day 9 part 1:", encoding.findError())
    print("Day 9 part 2:", encoding.getWeakness())
