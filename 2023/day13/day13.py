from typing import List, Optional, Tuple


class Springs:
    def getInput(self) -> List[Tuple[str, List[int]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        patternList = []
        pattern = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                if not line:
                    patternList.append(pattern)
                    pattern = []
                    continue
                pattern.append(line)
            patternList.append(pattern)
            return patternList

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.patternList = self.getInput()
        for pattern in self.patternList:
            print(pattern)

    def getTotal(self, isPart2: Optional[bool] = False) -> int:
        total = 0

        for pattern in self.patternList:
            m = len(pattern[0])
            n = len(pattern)
            for i in range(m - 1):
                reflectY = True
                length = min(m - i, i)
                for row in pattern:
                    print(row[i - length : i], row[i + 1 : i + 1 + length])
                    if row[i - length : i] != row[i + 1 : i + 1 + length]:
                        reflectY = False
                        break
                if reflectY:
                    lineY = i
            # for j in range(n - 1):
            #     reflectX = True
            #     length = min(n - j, j)
            #     for row in pattern:
            #         print(row[i - length : i], row[i + 1 : i + 1 + length])
            #         if row[i - length : i] != row[i + 1 : i + 1 + length]:
            #             reflectX = False
            #             break
            #     if reflectY:
            #         lineY = i

        return total


if __name__ == "__main__":
    springs = Springs(True)
    print("Day 13 part 1:", springs.getTotal())
    # print("Day 13 part 2:", springs.getTotal(True))
