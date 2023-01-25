from typing import TypedDict
import re
import math

class Monkey():

    def  __init__(self, MonkeyObj: TypedDict):
        self.items = MonkeyObj['items']
        self.operation = MonkeyObj['operation']
        self.test = MonkeyObj['test']
        self.result = MonkeyObj['result']
        self.itemsInspected = 0
        self.worry =  MonkeyObj['worry']
        # result arr: [false monkey, true monkey]

    def passItems(self):
        passInfo = {}
        for item in self.items:
            self.itemsInspected += 1
            item = self.operation(item) 
            item = item // 3 if self.worry else item
            divisible = item % self.test == 0
            if self.result[divisible] in passInfo:
                passInfo[self.result[divisible]].append(item)
            else:
                passInfo[self.result[divisible]] = [item]
        self.items = []
        return passInfo
    
    def recieveItems(self, items: list[int]):
        self.items += items

class MonkeyGame():
    
    def getInput(self):
        file1 = open('input.txt', 'r')
        file1 = open('input-test.txt', 'r')
        Lines = file1.readlines()
        data = []
        # Get input data
        for line in Lines:
            data.append(line.strip())
        return data

    def __init__(self, rounds: int, worry: bool = True) -> None:
        """ Main entry point of the app """
        self.inputData = self.getInput()
        self.rounds = rounds
        self.worry = worry
        self.Monkeys = []
        self.initializeMonkeys()
        self.maxInspected = [0,0]
    
    def getOperation(self, operation: str, value: int = 0):
        
        match  operation:
            case '+':
                return lambda x: x + value if value else x + x
            case '-':
                return lambda x: x - value if value else x - x
            case '*':
                return lambda x: x * value if value else x * x
            case '/':
                return lambda x: x / value if value else x / x
            case '%':
                return lambda x: x % value if value else x % x
            case '^':
                return lambda x: x ^ value if value else x ^ x
            case  _:
                return None
             
    def initializeMonkeys(self):
        currMonkey = {}

        for row in self.inputData:
            if row:
                arg1 = row.split()[0]
                if arg1 == 'Monkey':
                    if currMonkey:
                        newMonkey = Monkey(currMonkey)
                        self.Monkeys.append(newMonkey)
                    currMonkey = {}
                    currMonkey['result'] = [None,None]
                    currMonkey['worry'] = self.worry
                elif arg1 == 'Starting':
                    items = [int(x) for x in re.split(', |Starting items: ', row)[1:]]
                    currMonkey['items'] = items
                elif arg1 == 'Operation:':
                    operator = row.split()[4]
                    if row.split()[5].isdigit():
                        value = int(row.split()[5])
                        currMonkey['operation'] = self.getOperation(operator,value)
                    else:
                        currMonkey['operation'] = self.getOperation(operator)
                elif arg1 == 'Test:':
                    currMonkey['test'] = int(row.split()[3])
                elif arg1 == 'If':
                    monkeyNum = int(row.split()[5])                    
                    if  row.split()[1] == 'true:':
                        currMonkey['result'][1] = monkeyNum
                    elif row.split()[1] == 'false:':
                        currMonkey['result'][0] = monkeyNum
        newMonkey = Monkey(currMonkey)
        self.Monkeys.append(newMonkey)
    
    def playRound(self):
        for monkey in self.Monkeys:
            monkeyInfo = monkey.passItems()
            for monkeyNum in monkeyInfo:
                self.Monkeys[monkeyNum].recieveItems(monkeyInfo[monkeyNum])

    def  playGame(self):
        for _ in range(self.rounds):
            self.playRound()

    def getMonkeys(self):
        for i,monkey in  enumerate(self.Monkeys):
            print('Monkey #', i ,'--------------------------------')
            monkey.printInfo()

    def getInspectedTimes(self):
        for i,monkey in  enumerate(self.Monkeys):
            if monkey.itemsInspected > self.maxInspected[1]:
                self.maxInspected[1] = monkey.itemsInspected
                self.maxInspected.sort(reverse=True)
        return math.prod(self.maxInspected)

if __name__ == "__main__":
    """ This isexecuted when run from the command line """
    game1= MonkeyGame(20)
    game1.playGame()
    game2= MonkeyGame(10000, False)
    game2.playGame()
    print('Day 11 part 1:', game1.getInspectedTimes())
    print('Day 11 part 2:', game2.getInspectedTimes())
