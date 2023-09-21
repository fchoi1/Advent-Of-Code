from typing import List, Optional


def getInput(useTest) -> List[str]:
    inputFile = "input-test.txt" if useTest else "input.txt"
    with open(inputFile, "r") as file1:
        return [x.strip() for x in file1.readlines()]


def main(useTest: Optional[bool] = False) -> None:
    inputData = getInput(useTest)

    scorePt1 = scorePt2 = 0

    for round in inputData:
        [p1, p2] = round.split(" ")
        scorePt1 += calculateRound(p1, p2)
        scorePt2 += calculateRound2(p1, p2)

    print("day 2 part 1:", scorePt1)
    print("day 2 part 2:", scorePt2)


def calculateRound(player1: str, player2: str) -> int:
    gameMap = {"X": 1, "Y": 2, "Z": 3}
    match [player1, player2]:
        case ["A", "Z"] | ["B", "X"] | ["C", "Y"]:
            return 0 + gameMap[player2]
        case ["A", "X"] | ["B", "Y"] | ["C", "Z"]:
            return 3 + gameMap[player2]
        case ["A", "Y"] | ["B", "Z"] | ["C", "X"]:
            return 6 + gameMap[player2]
        case _:
            return 0


def calculateRound2(player1: str, end: str) -> int:
    gameMap = {"A": 1, "B": 2, "C": 3}
    match [player1, end]:
        case ["A", "X"] | ["B", "X"] | ["C", "X"]:
            return 0 + (gameMap[player1] + 1) % 3 + 1
        case ["A", "Y"] | ["B", "Y"] | ["C", "Y"]:
            return 3 + gameMap[player1]
        case ["A", "Z"] | ["B", "Z"] | ["C", "Z"]:
            return 6 + (gameMap[player1]) % 3 + 1
        case _:
            return 0


if __name__ == "__main__":
    main()
