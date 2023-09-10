from typing import Optional, List
import re

class Haversacks:
    def getInput(self) ->  List:
        inputFile = "input-test2.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            data = {}
            delimiters = "|".join(map(re.escape, [" bags contain ", " ", ", ", "."]))
            for line in file1.readlines():
                line = line.strip()

            return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.bags = self.getInput()

if __name__ == "__main__":
    haversacks = Haversacks()
    print("Day 8 part 1:")
    print("Day 8 part 2:")
