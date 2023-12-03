from typing import List, Optional


def getInput(useTest) -> List[str]:
    inputFile = "input-test.txt" if useTest else "input.txt"
    with open(inputFile, "r") as file1:
        return [x.strip() for x in file1]


def main(useTest: Optional[bool] = False) -> None:
    inputData = getInput(useTest)
    priorityMap = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 
            'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19,
            't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26, 'A': 27, 'B': 28, 
            'C': 29, 'D': 30, 'E': 31, 'F': 32, 'G': 33, 'H': 34, 'I': 35, 'J': 36, 'K': 37,
            'L': 38, 'M': 39, 'N': 40, 'O': 41, 'P': 42, 'Q': 43, 'R': 44, 'S': 45, 'T': 46,
            'U': 47, 'V': 48, 'W': 49, 'X': 50, 'Y': 51, 'Z': 52,
        }
    priorityPt1 = priorityPt2 = 0
    badgeList = []

    for rugsack in inputData:
        compartment1 = rugsack[: len(rugsack) // 2]
        compartment2 = rugsack[len(rugsack) // 2 :]
        priorityPt1 += priorityMap[findCommon(compartment1, compartment2)]
        badgeList.append(rugsack)

        if len(badgeList) == 3:
            priorityPt2 += priorityMap[
                findCommon(badgeList[0], badgeList[1], badgeList[2])
            ]
            badgeList = []

    print("day 3 part 1:", priorityPt1)
    print("day 3 part 2:", priorityPt2)


def findCommon(string1: str, string2: str, string3: str = "") -> str:
    unique = {}
    unique2 = {}
    for char in string1:
        if char not in unique:
            unique[char] = True

    for char in string2:
        if char in unique:
            if string3:
                unique2[char] = True
            else:
                return char

    for char in string3:
        if char in unique2:
            return char

    return ""


if __name__ == "__main__":
    main()
