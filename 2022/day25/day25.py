from typing import List, Optional


class Balloon:
    def getInput(self) -> List[str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                data.append(list(line.strip()))
            return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.snafu = self.getInput()

    def toSNAFU(self, num: int) -> str:
        snafu = ""
        digits = 1
        power = 2

        while num > power:
            power += 2 * (5**digits)
            digits += 1
        digits -= 1

        for i in range(digits, -1, -1):
            mutiplier = 5**i

            top = num + (mutiplier // 2) + mutiplier * 2
            index = top // mutiplier - 2

            snafu += "=-012"[index + 2]
            num -= (index) * mutiplier
        print(num)
        return snafu

    def fromSNAFU(self, SNAFU: str) -> int:
        n = 0
        for i, char in enumerate(reversed(SNAFU)):
            index = "=-012".index(char) - 2
            n += (5**i) * index
        return n

    def getFuel(self):
        n = 0
        for snafu in self.snafu:
            n += self.fromSNAFU(snafu)
        return self.toSNAFU(n)


if __name__ == "__main__":
    balloon = Balloon()
    print("Day 25 part 1:", balloon.getFuel())
