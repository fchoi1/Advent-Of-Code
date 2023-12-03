from typing import Optional, List, Tuple


class Scanner:
    def getInput(self) -> List[Tuple[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        lasers = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip().split(": ")
                lasers.append((int(line[0]), int(line[1])))
        return lasers

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.lasers = self.getInput()

    def getSeverity(self, delay: Optional[int] = 0) -> int:
        severity = 0
        for index, length in self.lasers[0:]:
            if (index + delay) % (length * 2 - 2) == 0:
                if delay != 0: # for Part 2
                    return 1
                severity += length * index
        return severity

    def getMinDelay(self) -> int:
        delay = 0
        while delay < 10_000_000 and self.getSeverity(delay) > 0:
            delay += 1
        return delay


if __name__ == "__main__":
    scanner = Scanner()
    print("Day 13 part 1:", scanner.getSeverity())
    print("Day 13 part 2:", scanner.getMinDelay())
