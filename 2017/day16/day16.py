from typing import Optional, List, Dict


class Promenade:
    def getInput(self) -> List[str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x for x in file1.readline().strip().split(",")]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.dance = self.getInput()
        self.reset()

    def reset(self) -> None:
        self.program = list("abcde") if self.useTest else list("abcdefghijklmnop")
        self.charMap = self.makeMap(self.program)
        self.start = 0

    def makeMap(self, string: str) -> Dict[str, int]:
        return {char: i for i, char in enumerate(string)}

    def runDance(self) -> None:
        for dance in self.dance:
            if dance[0] == "s":
                self.start = (self.start - int(dance[1:])) % len(self.program)
            elif dance[0] == "x":
                n1, n2 = dance[1:].split("/")
                p1 = (int(n1) + self.start) % len(self.program)
                p2 = (int(n2) + self.start) % len(self.program)

                self.charMap[self.program[p1]] = p2
                self.charMap[self.program[p2]] = p1
                self.program[p1], self.program[p2] = self.program[p2], self.program[p1]

            elif dance[0] == "p":
                n1, n2 = dance[1:].split("/")
                p1 = self.charMap[n1]
                p2 = self.charMap[n2]
                self.charMap[dance[1]], self.charMap[dance[3]] = (
                    self.charMap[dance[3]],
                    self.charMap[dance[1]],
                )
                self.program[p1], self.program[p2] = self.program[p2], self.program[p1]

    def getPosition(self, isPart2: Optional[bool] = False) -> int:
        self.reset()
        seen = set()
        seenList = []
        loop = 1_000_000_000 if isPart2 else 1
        for i in range(loop):
            self.runDance()
            doubleStr = "".join(self.program) * 2
            currProgram = doubleStr[self.start : self.start + len(self.program)]
            if currProgram in seen:
                break
            seen.add(currProgram)
            seenList.append(currProgram)
        index = 0 if i == 0 else loop % i
        return seenList[index - 1]


if __name__ == "__main__":
    promenade = Promenade()
    print("Day 16 part 1:", promenade.getPosition())
    print("Day 16 part 2:", promenade.getPosition(True))
