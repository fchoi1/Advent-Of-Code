from typing import List, Optional


class Library:
    def getInput(self) -> List[List[List[str]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        laser = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                laser.append(list(line))

            return laser

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.data = self.getInput()
        self.energized = set()
        print(self.data)

    def moveBeam(self, direction, pos):
        x, y = pos
        key = 
        pass

    def getTotal(self) -> int:
        total = 0

        return len(self.energized)


if __name__ == "__main__":
    library = Library(True)
    print("Day 16 part 1:", library.getTotal())
    print("Day 16 part 1:", library.getTotal())
