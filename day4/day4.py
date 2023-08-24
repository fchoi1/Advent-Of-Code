from typing import List


def getInput() -> List[str]:
    file1 = open("input.txt", "r")
    Lines = file1.readlines()
    data = []
    # Get input data
    for line in Lines:
        data.append(line.strip())
    return data


def main() -> None:
    """Main entry point of the app"""
    inputData = getInput()

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
    """This is executed when run from the command line"""
    main()
