from typing import List, Optional
import re


class Monkeys:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        constants = {}
        equations = {}
        delimiters = [": ", " "]
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                line = re.split("|".join(map(re.escape, delimiters)), line.strip())
                if len(line) == 2:
                    constants[line[0]] = int(line[1])
                else:
                    equations[line[0]] = [line[1], line[3], line[2]]

            return [constants, equations]

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

    def evaluateEquation(self, target: str) -> int:
        first, second, op = self.equations[target]

        firstNum = (
            self.constants[first]
            if first in self.constants
            else self.evaluateEquation(first)
        )

        secondNum = (
            self.constants[second]
            if second in self.constants
            else self.evaluateEquation(second)
        )

        return self.operations[op](firstNum, secondNum)

    def evaluateEquation2(self, target: str, ops: List[str]) -> List:
        print('target', target)
        if target not in self.equations:
            return None
        
        first, second, op = self.equations[target]
        
        if first in self.constants:
            firstNum = self.constants[first]

        firstNum = self.evaluateEquation2(first, ops)

        if second in self.constants:
            secondNum = self.constants[second]

        secondNum = self.evaluateEquation2(second, ops)
       

        if not isinstance(firstNum, int) and not isinstance(secondNum, int):
            ops.append(['*', op, '*'])
            return ops
        
        if not isinstance(firstNum, int):
            ops.append([op, secondNum])
            return ops

        if not isinstance(secondNum, int):
            ops.append([firstNum, op])
            return ops

        print('firs', firstNum, 'second', secondNum)
        # ops.append(self.operations[op](firstNum, secondNum))
        return self.operations[op](firstNum, secondNum)


    def getRoot(self):
        return self.evaluateEquation("root")

    def updateConstant(self, target: str) -> int:
        # delete is from constant
        del self.constants[target]
        print(self.evaluateEquation2("sjmn", []))
        print(self.evaluateEquation2("pppw", []))

    def getHumn(self):
        self.updateConstant("humn")


if __name__ == "__main__":
    """This is executed when run from the command line"""
    monkeys = Monkeys(True)
    # print("Day 21 part 1:", monkeys.getRoot())
    print("Day 21 part 2:", monkeys.getHumn())
    # Total Runtime ~ 3.5 Seconds
