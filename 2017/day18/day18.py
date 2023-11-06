from typing import Optional, List, Union, Deque, Dict
from collections import defaultdict, deque


class Duet:
    def getInput(self) -> List[Union[str, int]]:
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
        self.recover = self.count = 0

    def getRecover(self) -> int:
        register = defaultdict(int)
        index = recover = 0
        while 0 <= index < len(self.commands):
            cmd = self.commands[index]
            if cmd[0] in ["snd", "rcv"]:
                val = cmd[1] if isinstance(cmd[1], int) else register[cmd[1]]
            else:
                val = cmd[2] if isinstance(cmd[2], int) else register[cmd[2]]
            if cmd[0] == "snd":
                recover = val
            elif cmd[0] == "rcv":
                if val != 0:
                    return recover
            elif cmd[0] == "set":
                register[cmd[1]] = val
            elif cmd[0] == "add":
                register[cmd[1]] += val
            elif cmd[0] == "mul":
                register[cmd[1]] *= val
            elif cmd[0] == "mod":
                register[cmd[1]] %= val
            elif cmd[0] == "jgz":
                jmp = cmd[1] if isinstance(cmd[1], int) else register[cmd[1]]
                if jmp > 0:
                    index += val
                    continue
            index += 1
        return recover

    def runProgram(
        self,
        i: int,
        register: Dict[str, int],
        send: Deque[int],
        recieve: Deque[int],
        count: bool,
    ) -> int:
        while 0 <= i < len(self.commands):
            cmd = self.commands[i]
            if cmd[0] in ["snd", "rcv"]:
                val = cmd[1] if isinstance(cmd[1], int) else register[cmd[1]]
            else:
                val = cmd[2] if isinstance(cmd[2], int) else register[cmd[2]]
            if cmd[0] == "snd":
                if count:
                    self.count += 1
                send.append(val)
            elif cmd[0] == "rcv":
                if recieve:
                    register[cmd[1]] = recieve.popleft()
                else:
                    return i
            elif cmd[0] == "set":
                register[cmd[1]] = val
            elif cmd[0] == "add":
                register[cmd[1]] += val
            elif cmd[0] == "mul":
                register[cmd[1]] *= val
            elif cmd[0] == "mod":
                register[cmd[1]] %= val
            elif cmd[0] == "jgz":
                jmp = cmd[1] if isinstance(cmd[1], int) else register[cmd[1]]
                if jmp > 0:
                    i += val
                    continue
            i += 1
        return i

    def countSends(self) -> int:
        queue0, queue1 = deque(), deque()
        register1, register0 = defaultdict(lambda: 1), defaultdict(int)
        p0 = self.runProgram(0, register1, queue1, queue0, False)
        p1 = self.runProgram(0, register0, queue0, queue1, True)
        while queue0 or queue1:
            p0 = self.runProgram(p0, register1, queue1, queue0, False)
            p1 = self.runProgram(p1, register0, queue0, queue1, True)
        return self.count


if __name__ == "__main__":
    duet = Duet()
    print("Day 18 part 1:", duet.getRecover())
    print("Day 18 part 2:", duet.countSends())
