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
        self.useTest = useTest
        self.constants, self.equations = self.getInput()

        self.operations = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
        }
        self.reverseOp = {
            "+": "-",
            "-": "+",
            "*": "/",
            "/": "*"
        }

    def evaluateEquation(self, target: str, ops: List[str]) -> List[str] | int:
        if target not in self.equations:
            return None
        
        first, second, op = self.equations[target]
        
        firstNum = (
            self.constants[first] if first in self.constants
                else self.evaluateEquation(first, ops)
        )
        secondNum = (
            self.constants[second] if second in self.constants 
                else self.evaluateEquation(second, ops)
        )

        if isinstance(firstNum, (int, float)) and isinstance(secondNum, (int,float)):
            return self.operations[op](firstNum, secondNum)
        
        if isinstance(firstNum, list):
            firstNum.append([None, op, secondNum])
            return firstNum
        elif isinstance(secondNum, list):
            secondNum.append([firstNum, op, None])
            return secondNum
        
        ops.append([firstNum, op, secondNum])
        return ops

    def getRoot(self):
        return self.evaluateEquation("root", [])        

    def getConstant(self, target: Optional[str] = 'humn'):
        if target in self.constants:
            del self.constants[target]

        num1, num2, op = self.equations['root']
        
        value1 = self.evaluateEquation(num1, [])
        value2 = self.evaluateEquation(num2, [])

        operationList = None
        targetVal = None

        if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
            return self.operations[op](value1, value2)

        if isinstance(value1, list):
            operationList = value1
            targetVal = value2

        elif isinstance(value2, list):
            operationList = value2
            targetVal = value1
            
        if operationList:
            for num1, op, num2 in reversed(operationList):
                
                reverseOp = self.reverseOp[op]
                x = targetVal
                y = num2 if not num1 else num1
                
                # Special case for - and / operations (not comuntative)
                if not num2 and op in ['/', '-']:
                    reverseOp = op
                    x = num1 
                    y = targetVal
                    
                targetVal = self.operations[reverseOp](x, y)
        return targetVal


if __name__ == "__main__":
    monkeys = Monkeys()
    print("Day 21 part 1:", monkeys.getRoot())
    print("Day 21 part 2:", monkeys.getConstant())
