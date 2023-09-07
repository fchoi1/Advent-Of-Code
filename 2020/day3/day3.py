from typing import List, Optional, Tuple


class Toboggan:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
            data = []
            for line in Lines:
                data.append(line.strip())
        return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.trees = self.getInput()
        self.width = len(self.trees[0])
        self.slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    def findTree(self, slope: Optional[Tuple[int]] = (3, 1)):
        tree_count = 0
        x, y = 0, 0

        for row in self.trees:
            if y % slope[1] == 0:
                if row[x % self.width] == "#":
                    tree_count += 1
                x += slope[0]
            y += 1

        return tree_count

    def getTrees(self):
        product = 1
        for slope in self.slopes:
            product *= self.findTree(slope)
        return product


if __name__ == "__main__":
    toboggan = Toboggan(False)
    print("Day 3 part 1:", toboggan.findTree())
    print("Day 3 part 2:", toboggan.getTrees())
