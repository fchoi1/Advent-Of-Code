from typing import List, Optional, Tuple, Union, Dict


class Registers:
    def getInput(self) -> Tuple[Union[Dict[str, int], List[str]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        registers = {}
        commands = []
        with open(inputFile, "r") as file1:
            for line in file1:
                s = line.strip().split(" ")
                registers[s[0]] = 0
                commands.append([s[0], s[1], int(s[2]), s[4], s[5], int(s[6])])
        return registers, commands

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.registers, self.commands = self.getInput()
        self.currentLargest = self.largest = 0
        self.runProgram()

    def runProgram(self) -> None:
        operators = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            "<": lambda a, b: a < b,
            "<=": lambda a, b: a <= b,
            ">": lambda a, b: a > b,
            ">=": lambda a, b: a >= b,
        }
        for command in self.commands:
            x = self.registers[command[3]]
            y = command[5]
            sign = 1 if command[1] == "inc" else -1
            if operators[command[4]](x, y):
                self.registers[command[0]] += sign * command[2]
                self.largest = max(self.largest, self.registers[command[0]])
        self.currentLargest = max(self.registers.values())

    def getCurrentLargest(self) -> int:
        return self.currentLargest

    def getLargest(self) -> int:
        return self.largest


if __name__ == "__main__":
    registers = Registers()
    print("Day 8 part 1:", registers.getCurrentLargest())
    print("Day 8 part 2:", registers.getLargest())
