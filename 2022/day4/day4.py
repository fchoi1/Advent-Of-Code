from typing import List, Optional


def getInput(useTest) -> List[str]:
    inputFile = "input-test.txt" if useTest else "input.txt"
    with open(inputFile, "r") as file1:
        return [x.strip() for x in file1.readlines()]


def main(useTest: Optional[bool] = False) -> None:
    inputData = getInput(useTest)

    count1 = count2 = 0
    for pair in inputData:
        [p1, p2] = pair.split(",")
        p1 = [int(x) for x in p1.split("-")]
        p2 = [int(x) for x in p2.split("-")]
        if fullyEnclosed(p1, p2):
            count1 += 1
        if overlaped(p1, p2):
            count2 += 1

    print("day 4 part 1:", count1)
    print("day 4 part 2:", count2)


def fullyEnclosed(p1: List[int], p2: List[int]) -> bool:
    return (p1[0] >= p2[0] and p1[1] <= p2[1]) or (p2[0] >= p1[0] and p2[1] <= p1[1])


def overlaped(p1: List[int], p2: List[int]) -> bool:
    return not ((p1[1] < p2[0]) or (p2[1] < p1[0]))


if __name__ == "__main__":
    main()
