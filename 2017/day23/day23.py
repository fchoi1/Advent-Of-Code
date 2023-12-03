from typing import Optional, List
from collections import defaultdict
from math import sqrt


class Coprocessor:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        commands = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip().split(" ")
                line[1:] = [
                    int(item) if item.lstrip("-").isdigit() else item
                    for item in line[1:]
                ]
                commands.append(line)
        return commands

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.commands = self.getInput()

    def isPrime(self, n: int) -> bool:
        if n % 2 == 0:
            return False
        for i in range(3, int(sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    def runCommands(self, skip: bool) -> None:
        index = mulCount = 0
        maxLen = len(self.commands)
        while 0 <= index < maxLen:
            cmd = self.commands[index]
            if skip and index == 19:
                self.register["e"] = self.register["b"]
                self.register["f"] = self.isPrime(self.register["b"])
                index += 1
                continue

            if skip and index == 23:
                self.register["d"] = self.register["b"]
                index += 1
                continue

            Y = cmd[2] if isinstance(cmd[2], int) else self.register[cmd[2]]
            if cmd[0] == "set":
                self.register[cmd[1]] = Y
            elif cmd[0] == "sub":
                self.register[cmd[1]] -= Y
            elif cmd[0] == "mul":
                mulCount += 1
                self.register[cmd[1]] *= Y
            elif cmd[0] == "jnz":
                jmp = cmd[1] if isinstance(cmd[1], int) else self.register[cmd[1]]
                if jmp != 0:
                    index += Y
                    continue
            index += 1
        self.mulCount = mulCount

    def getRegisterH(self) -> int:
        self.register = defaultdict(int)
        self.register["a"] = 1
        self.runCommands(True)
        return self.register["h"]

    def getMulCount(self) -> int:
        self.register = defaultdict(int)
        self.runCommands(False)
        return self.mulCount


if __name__ == "__main__":
    coprocessor = Coprocessor()
    print("Day 23 part 1:", coprocessor.getMulCount())
    print("Day 23 part 2:", coprocessor.getRegisterH())
