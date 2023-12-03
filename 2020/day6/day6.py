from typing import List, Optional


class Customs:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            group, data = [], []
            for line in file1:
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

    # set on string
    def getYes(self) -> int:
        return sum(len(set("".join(group))) for group in self.forms)

    def getYes2(self) -> int:
        return sum(len(set.intersection(*(set(person) for person in group))) for group in self.forms)


if __name__ == "__main__":
    customs = Customs()
    print("Day 6 part 1:", customs.getYes())
    print("Day 6 part 2:", customs.getYes2())
