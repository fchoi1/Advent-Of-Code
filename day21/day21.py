from typing import List, Optional
import re


class Monkeys:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        constant = {}
        equations = {}
        delimiters = [":  ", " "]
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                line = re.split("|".join(map(re.escape, delimiters)), line.strip())
                if len(line) == 2:
                    constant[line[0]] = int(line[1])
                else:
                    equations[line[0]] = [line[1], line[3], line[2]]

            return [constant, equations]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        """Main entry point of the app"""
        self.useTest = useTest
        self.constants, self.equations = self.getInput()

        self.operations = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
        }

        
        # result = operator_mapping[operator](operand1, operand2)



if __name__ == "__main__":
    """This is executed when run from the command line"""
    monkeys = Monkeys(True)
    print("Day 21 part 1:")
    print("Day 21 part 2:")
    # Total Runtime ~ 3.5 Seconds
