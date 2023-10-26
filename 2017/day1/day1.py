from typing import List, Optional


class Captcha:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(x.strip()) for x in file1.readline()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.numList = self.getInput()

    def getSum(self, isPart2: Optional[bool] = False) -> int:
        length = len(self.numList)
        mid = length // 2
        prev = self.numList[mid] if isPart2 else self.numList[-1]
        total = 0
        for i in range(length):
            n = self.numList[i]
            if prev == n:
                total += n
            mid = (mid + 1) % length
            prev = self.numList[mid] if isPart2 else n
        return total


if __name__ == "__main__":
    captcha = Captcha()
    print("Day 1 part 1:", captcha.getSum())
    print("Day 1 part 2:", captcha.getSum(True))
