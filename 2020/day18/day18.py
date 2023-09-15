from typing import Optional, List, Callable, Union
from functools import reduce


class Operation:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1:
                data.append(line.strip().replace("(", "( ").replace(")", " )").split(" "))
                pass
        return data

    def __init__(self, useTest: Optional[bool] = False, rounds: Optional[int] = 6) -> None:
        self.useTest = useTest
        self.expressions = self.getInput()

    def getOperation(self, operation: str) -> Callable[[int], Union[int, float]] | None:
        match operation:
            case "+":
                return lambda x, y: x + y
            case "*":
                return lambda x, y: x * y
            case _:
                return None

    def evaluate(self, expression: List[str]) -> int:
        stack = []
        currVal, currOp = 0, ""

        for val in expression:
            if val in "+*":
                currOp = val
                continue
            elif val == "(":
                stack.append((currVal, currOp))
                currVal, currOp = 0, ""
                continue
            elif val == ")":
                prevVal, prevOp = stack.pop()
                currVal = self.getOperation(prevOp)(prevVal, currVal) if prevOp else currVal
                continue
            currVal = self.getOperation(currOp)(currVal, int(val)) if currOp else int(val)

        return currVal

    def evaluate2(self, expression: List[str]) -> int:
        stack = []
        currExpression = []

        for val in expression:
            if val == "(":
                stack.append(currExpression)
                currExpression = []
                continue
            elif val == ")":
                bracketVal = self.flatEvaluate(currExpression)
                currExpression = stack.pop()
                currExpression.append(bracketVal)
                continue
            currExpression.append(val)

        return self.flatEvaluate(currExpression)

    def flatEvaluate(self, flatExpression: List[str]) -> int:
        expression = []
        multiply = False
        for val in flatExpression:
            if val == "+":
                multiply = True
            elif multiply:
                expression[-1] += int(val)
                multiply = False
            elif val != "*":
                expression.append(int(val))
        return reduce(lambda x, y: x * y, expression)

    def getSum(self, useOrder: Optional[bool] = False) -> int:
        evaluateFn = self.evaluate2 if useOrder else self.evaluate
        return sum(evaluateFn(expression) for expression in self.expressions)


if __name__ == "__main__":
    operation = Operation()
    print("Day 18 part 1:", operation.getSum())
    print("Day 18 part 2:", operation.getSum(True))
