from typing import Optional, List


class Coprocessor:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        commands = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                line = line.strip().split(" ")
                line[1:] = [
                    int(item) if item.lstrip("-").isdigit() else item
                    for item in line[1:]
                ]
                commands.append(line)
        return commands

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.commands = self.getInput()

    def getMulCount(self) -> int:
        return 1


if __name__ == "__main__":
    coprocessor = Coprocessor()
    print("Day 24 part 1:", coprocessor.getMulCount())
