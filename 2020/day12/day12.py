from typing import Optional, List, 


class Ferry:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                data.append(list(line.strip()))
        return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.seats = self.getInput()

if __name__ == "__main__":
    ferry = Ferry()
    print("Day 12 part 1:")
    print("Day 12 part 2:" )
