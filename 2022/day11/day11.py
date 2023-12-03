from typing import TypedDict, Dict, List, Optional, Callable, Union
import re
from math import gcd, prod


class Monkey:
    def __init__(self, MonkeyObj: TypedDict) -> None:
        self.items = MonkeyObj["items"]
        self.operation = MonkeyObj["operation"]
        self.test = MonkeyObj["test"]
        self.result = MonkeyObj["result"]
        self.itemsInspected = 0
        self.worry = MonkeyObj["worry"]

    def updateDivisor(self, divisor: int) -> None:
        self.modulo = divisor

    def passItems(self) -> Dict[str, List[int]]:
        passInfo = {}
        for item in self.items:
            self.itemsInspected += 1
            item = self.operation(item)
            item = item // 3 if self.worry else item
            divisible = item % self.test == 0
            # too large item reduce it
            item = item % self.modulo
            if self.result[divisible] in passInfo:
                passInfo[self.result[divisible]].append(item)
            else:
                passInfo[self.result[divisible]] = [item]
        self.items = []
        return passInfo

    def recieveItems(self, items: list[int]) -> None:
        self.items += items


class MonkeyGame:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x.strip() for x in file1]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.inputData = self.getInput()
        self.reset()

    def reset(self) -> None:
        self.Monkeys = []
        self.maxInspected = [0, 0]
        self.testList = []

    def updateLCM(self) -> None:
        lcm = 1
        for i in self.testList:
            lcm = lcm * i // gcd(lcm, i)
        for monkey in self.Monkeys:
            monkey.updateDivisor(lcm)

    def getOperation(
        self, operation: str, value: int = 0
    ) -> Callable[[int], Union[int, float]] | None:
        match operation:
            case "+":
                return lambda x: x + value if value else x + x
            case "-":
                return lambda x: x - value if value else x - x
            case "*":
                return lambda x: x * value if value else x * x
            case "/":
                return lambda x: x / value if value else x / x
            case "%":
                return lambda x: x % value if value else x % x
            case "^":
                return lambda x: x ^ value if value else x ^ x
            case _:
                return None

    def initializeMonkeys(self) -> None:
        currMonkey = {}

        for row in self.inputData:
            if row:
                arg1 = row.split()[0]
                if arg1 == "Monkey":
                    if currMonkey:
                        newMonkey = Monkey(currMonkey)
                        self.Monkeys.append(newMonkey)
                    currMonkey = {}
                    currMonkey["result"] = [None, None]
                    currMonkey["worry"] = self.worry
                elif arg1 == "Starting":
                    items = [int(x) for x in re.split(", |Starting items: ", row)[1:]]
                    currMonkey["items"] = items
                elif arg1 == "Operation:":
                    operator = row.split()[4]
                    if row.split()[5].isdigit():
                        value = int(row.split()[5])
                        currMonkey["operation"] = self.getOperation(operator, value)
                    else:
                        currMonkey["operation"] = self.getOperation(operator)
                elif arg1 == "Test:":
                    currMonkey["test"] = int(row.split()[3])
                    self.testList.append(int(row.split()[3]))
                elif arg1 == "If":
                    monkeyNum = int(row.split()[5])
                    if row.split()[1] == "true:":
                        currMonkey["result"][1] = monkeyNum
                    elif row.split()[1] == "false:":
                        currMonkey["result"][0] = monkeyNum
        newMonkey = Monkey(currMonkey)
        self.Monkeys.append(newMonkey)
        self.updateLCM()

    def playRound(self) -> None:
        for monkey in self.Monkeys:
            monkeyInfo = monkey.passItems()
            for monkeyNum in monkeyInfo:
                self.Monkeys[monkeyNum].recieveItems(monkeyInfo[monkeyNum])

    def playGame(self, isPart2: Optional[bool] = False) -> None:
        if isPart2:
            rounds = 10000
        else:
            rounds = 20
        for _ in range(rounds):
            self.playRound()

    def getInspectedTimes(self, isPart2: Optional[bool] = False) -> int:
        self.worry = not isPart2
        self.reset()
        self.initializeMonkeys()
        self.playGame(isPart2)
        for monkey in self.Monkeys:
            if monkey.itemsInspected > self.maxInspected[1]:
                self.maxInspected[1] = monkey.itemsInspected
                self.maxInspected.sort(reverse=True)
        return prod(self.maxInspected)


if __name__ == "__main__":
    """This isexecuted when run from the command line"""
    monkeyGame = MonkeyGame()
    print("Day 11 part 1:", monkeyGame.getInspectedTimes())
    print("Day 11 part 2:", monkeyGame.getInspectedTimes(True))
