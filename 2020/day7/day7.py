from typing import List, Optional


class Haversacks:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            group, data = [], []
            for line in file1.readlines():
                if not line.strip():
                    data.append(group)
                    group = []
                    continue
                group.append(line.strip())
            data.append(group)
            return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.forms = self.getInput()


if __name__ == "__main__":
    haversacks = Haversacks()
    print("Day 7 part 1:")
    # print("Day 7 part 2:",)
