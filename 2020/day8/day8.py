from typing import Optional, List, Tuple


class Console:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            data = []
            for line in file1.readlines():
                line = line.strip().split(" ")
                data.append((line[0], int(line[1])))

            return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.console = self.getInput()
        self.length = len(self.console)
        self.visited = set()

    def getAcc(self) -> int:
        start = 0
        self.visited = set()
        acc = 0
        while start not in self.visited and start < self.length:
            command, val = self.console[start]
            self.visited.add(start)
            if command == "jmp":
                start = (start + val) % self.length
                continue
            if command == "acc":
                acc += val
            start += 1
        return acc

    def isLoop(self, index: int) -> bool:
        while index not in self.visited and index < self.length:
            command, val = self.console[index]
            if command == "jmp":
                index = index + val
                continue
            index += 1
        return index < self.length

    def fixProgram(self) -> int:
        index = -1
        correct = ""

        for n in self.visited:
            command, val = self.console[n]
            if command == "jmp":
                if not self.isLoop(n + 1):
                    correct = "nop"
                    index = n
                    break

            elif command == "nop":
                if not self.isLoop(n + val):
                    correct = "jmp"
                    index = n
                    break

        if index == -1:
            return -1
        self.console[index] = (correct, val)

        return self.getAcc()


if __name__ == "__main__":
    console = Console()
    print("Day 8 part 1:", console.getAcc())
    print("Day 8 part 2:", console.fixProgram())
