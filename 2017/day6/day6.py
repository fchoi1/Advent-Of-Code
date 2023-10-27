from typing import List, Optional, Tuple, Union


class Debugger:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(n) for n in (file1.readline().strip().split())]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.memory = self.getInput()
        self.length = len(self.memory)
        self.cycle1, self.cycleKey = self.getCycles("")
        self.cycle2, self.cycleKey = self.getCycles(self.cycleKey)

    def getCycles(self, cycleKey: str) -> Tuple[Union[int, str]]:
        seen = set()
        cycle = 0
        key = cycleKey
        while key not in seen:
            seen.add(key)
            currMax = max(self.memory)
            currIndex = self.memory.index(currMax)
            self.memory[currIndex] = 0

            part, remain = divmod(currMax, self.length)
            for i in range(self.length):
                index = (i + currIndex + 1) % self.length
                self.memory[index] += part + int(i < remain)
            key = ",".join(map(str, self.memory))
            cycle += 1
        return cycle, key

    def getCycle1(self) -> int:
        return self.cycle1

    def getCycle2(self) -> int:
        return self.cycle2


if __name__ == "__main__":
    debugger = Debugger()
    print("Day 6 part 1:", debugger.getCycle1())
    print("Day 6 part 2:", debugger.getCycle2())
