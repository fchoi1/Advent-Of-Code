from typing import Optional, List


class Generators:
    def getInput(self) -> str:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return file1.readline().strip()

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.key = self.getInput()

    def getUsed(self) -> int:
        return 1


if __name__ == "__main__":
    generators = Generators(True)
    print("Day 15 part 1:", Generators.getUsed())
    # print("Day 15 part 2:", generators.getRegions())
