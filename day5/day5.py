from typing import List
import re
from copy import deepcopy


def getInput() -> List[str]:
    file1 = open("input.txt", "r")
    # file1 = open('input-test.txt', 'r')
    Lines = file1.readlines()
    data = []
    # Get input data
    for line in Lines:
        data.append(line.strip())
    return data


def main() -> None:
    """Main entry point of the app"""
    inputData = getInput()

    """
                    [B] [L]     [J]    
                [B] [Q] [R]     [D] [T]
                [G] [H] [H] [M] [N] [F]
            [J] [N] [D] [F] [J] [H] [B]
        [Q] [F] [W] [S] [V] [N] [F] [N]
    [W] [N] [H] [M] [L] [B] [R] [T] [Q]
    [L] [T] [C] [R] [R] [J] [W] [Z] [L]
    [S] [J] [S] [T] [T] [M] [D] [B] [H]
    1   2   3   4   5   6   7   8   9 

        [D]    
    [N] [C]    
    [Z] [M] [P]
    1   2   3 

    """
    stackdata = [
        ["S", "L", "W"],
        ["J", "T", "N", "Q"],
        ["S", "C", "H", "F", "J"],
        ["T", "R", "M", "W", "N", "G", "B"],
        ["T", "R", "L", "S", "D", "H", "Q", "B"],
        ["M", "J", "B", "V", "F", "H", "R", "L"],
        ["D", "W", "R", "N", "J", "M"],
        ["B", "Z", "T", "F", "H", "N", "D", "J"],
        ["H", "L", "Q", "N", "B", "F", "T"],
    ]
    stackdataTest = [["Z", "N"], ["M", "C", "D"], ["P"]]

    stack1 = deepcopy(stackdata)
    stack2 = deepcopy(stackdata)
    word1 = word2 = ""

    for line in inputData:
        instruction = [int(x) for x in re.split("move | from | to ", line)[1:]]
        stack1 = updateStack(instruction, stack1)
        stack2 = updateStack2(instruction, stack2)

    for stack in stack1:
        word1 += stack[len(stack) - 1]

    for stack in stack2:
        word2 += stack[len(stack) - 1]

    wordTest = ""
    for stack in stackdataTest:
        wordTest += stack[len(stack) - 1]
    print("day 5 part 1:", word1)
    print("day 5 part 2:", word2)


def updateStack(instruction: list[int], stack: List[List[str]]) -> List[List[str]]:
    for _ in range(instruction[0]):
        letter = stack[instruction[1] - 1].pop()
        stack[instruction[2] - 1].append(letter)
    return stack


def updateStack2(instruction: list[int], stack: List[List[str]]) -> List[List[str]]:
    index = len(stack[instruction[1] - 1]) - instruction[0]
    for _ in reversed(range(instruction[0])):
        letter = stack[instruction[1] - 1].pop(index)
        stack[instruction[2] - 1].append(letter)
    return stack


if __name__ == "__main__":
    """This is executed when run from the command line"""
    main()
