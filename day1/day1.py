from typing import List

def getInput() -> List[str]:
    file1 = open('input.txt', 'r')
    Lines = file1.readlines()
    data = []
    # Get input data
    for line in Lines:
        data.append(line.strip())
    return data

def main() -> None:
    """ Main entry point of the app """
    inputData = getInput()

    maxCalories = [float("-inf")] * 3
    currentCal = 0
    for data in inputData:
        if data:
            currentCal += int(data)
        else:
            if currentCal >= maxCalories[2]:
                maxCalories[2] = currentCal
                maxCalories = sortCal(maxCalories)
            currentCal = 0
    
    print('day 1 part 1:', maxCalories[0])
    print('day 1 part 2:', sum(maxCalories))

def sortCal(calories: List[int]) -> List[int]:
    return sorted(calories, reverse=True)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()