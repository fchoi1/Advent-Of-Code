from typing import List, Optional, Tuple


class CPU:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(line.strip()) for line in file1.readlines()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest

    def getSteps(self, isPart2: Optional[bool] = False) -> int:
        self.jumpList = self.getInput()
        steps = index = 0

        while 0 <= index < len(self.jumpList):
            jump = self.jumpList[index] 
            offset = 1
            if isPart2:
                offset = -1 if jump >= 3 else 1 
            self.jumpList[index], index, = jump + offset , jump + index
            steps += 1
        return steps


if __name__ == "__main__":
    cpu = CPU()
    print("Day 5 part 1:", cpu.getSteps())
    print("Day 5 part 2:", cpu.getSteps(True))
    # Total Runtime ~7.41s
