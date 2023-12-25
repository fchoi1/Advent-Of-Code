from typing import List, Optional, Tuple, Dict


class Aplenty:
    def getInput(self) -> Tuple[Dict[List[str]], List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        workflows = {}
        inputs = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()

            return workflows, inputs

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.workflows, self.inputs = self.getInput()

    def getTotal(self) -> int:
        total = 0
        return total


if __name__ == "__main__":
    aplenty = Aplenty(True)
    print("Day 19 part 1:", aplenty.getTotal())
    # Total Runtime ~1.6s
