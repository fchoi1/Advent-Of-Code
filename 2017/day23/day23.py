from typing import Optional, List
from collections import defaultdict


class Coprocessor:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        commands = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
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

    def getMulCount(self) -> int:
        self.register = defaultdict(int)
        self.runCommands()
        return self.mulCount

    def runCommands(self) -> None:
        index = mulCount = 0
        maxLen = len(self.commands)
        count = 0
        while 0 <= index < 25:
            # if count > 60:
            #     break
            # count += 1
            cmd = self.commands[index]
            # print(index, cmd, self.register)
            if index == 11:
                self.register["e"] = abs(self.register["b"])
                self.register["g"] = 0
                self.register["f"] = 0
                index = 19
                # print("skip", self.register)

            if index == 23:
                self.register["d"] = self.register["e"]
                self.register["g"] = 0
                index += 1
                print("skip", self.register)
            # break

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
        print("end", self.register)
        self.mulCount = mulCount

    def getRegisterH(self) -> int:
        self.register = defaultdict(int)
        self.register["a"] = 1
        self.runCommands()
        return self.register["h"]


if __name__ == "__main__":
    coprocessor = Coprocessor()
    # print("Day 23 part 1:", coprocessor.getMulCount())
    print("Day 23 part 2:", coprocessor.getRegisterH())
