from typing import Optional, List


class Generators:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(x.strip().split(" ")[-1]) for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.genA, self.genB = self.getInput()
        self.factorA = 16807
        self.factorB = 48271
        self.product = 2147483647

    def compare16Bit(self, num1: int, num2: int) -> bool:
        n1 = num1 & 0xFFFF
        n2 = num2 & 0xFFFF
        return n1 == n2

    def getNextValue(self, num: int, gen: str, isPart2: bool) -> int:
        multiple = 4 if gen == "A" else 8
        factor = self.factorA if gen == "A" else self.factorB
        num = (num * factor) % self.product

        if not isPart2:
            return num

        while num % multiple != 0:
            num = (num * factor) % self.product
        return num

    def getPairs(self, isPart2: Optional[bool] = False) -> int:
        self.genA, self.genB = self.getInput()
        loops = 5_000_000 if isPart2 else 40_000_000
        count = pairs = 0
        while count < loops:
            if self.compare16Bit(self.genA, self.genB):
                pairs += 1
            self.genA = self.getNextValue(self.genA, "A", isPart2)
            self.genB = self.getNextValue(self.genB, "B", isPart2)
            count += 1
        return pairs


if __name__ == "__main__":
    generators = Generators()
    print("Day 15 part 1:", generators.getPairs())
    print("Day 15 part 2:", generators.getPairs(True))
    # Total Runtime ~ 40s
