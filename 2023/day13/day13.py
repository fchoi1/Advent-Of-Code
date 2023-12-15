from typing import List, Optional


class Mirrors:
    def getInput(self) -> List[List[List[str]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        pList = []
        p = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                if not line:
                    pList.append(p)
                    p = []
                    continue
                p.append(line)
            pList.append(p)
            return pList

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.patternList = self.getInput()
        self.vert = [[0] * len(self.patternList) for _ in range(2)]
        self.hor = [[0] * len(self.patternList) for _ in range(2)]
        self.getMirrors()
        self.getMirrors(True)

    def getMirrors(self, getSecond: Optional[bool] = False) -> None:
        for k, pattern in enumerate(self.patternList):
            m = len(pattern[0])
            n = len(pattern)
            for i in range(1, m):
                length = min(m - i, i)
                byOne = False
                if getSecond and self.vert[not getSecond][k] == i:
                    continue
                for row in pattern:
                    str1 = row[i - length : i]
                    str2 = row[i : i + length][::-1]
                    if getSecond:
                        count = self.getDiff(str1, str2)
                        if (str1 != str2 and byOne) or count > 1:
                            break
                        if count == 1:
                            byOne = True
                    else:
                        if str1 != str2:
                            break
                else:
                    self.vert[getSecond][k] = i
                    continue
            for j in range(1, n):
                length = min(n - j, j)
                byOne = False
                if getSecond and self.hor[not getSecond][k] == j:
                    continue
                for i in range(m):
                    str1 = "".join(col[i] for col in pattern[j - length : j])
                    str2 = "".join(col[i] for col in pattern[j : j + length][::-1])
                    if getSecond:
                        count = self.getDiff(str1, str2)
                        if (str1 != str2 and byOne) or count > 1:
                            break
                        if count == 1:
                            byOne = True
                    else:
                        if str1 != str2:
                            break
                else:
                    self.hor[getSecond][k] = j

    def getDiff(self, str1: str, str2: str) -> int:
        return sum(1 for char1, char2 in zip(str1, str2) if char1 != char2)

    def getTotal(self, isPart2: Optional[bool] = False) -> int:
        return sum(self.hor[isPart2]) * 100 + sum(self.vert[isPart2])


if __name__ == "__main__":
    mirrors = Mirrors()
    print("Day 13 part 1:", mirrors.getTotal())
    print("Day 13 part 2:", mirrors.getTotal(True))
