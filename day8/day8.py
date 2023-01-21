def getInput():
    file1 = open('input.txt', 'r')
    Lines = file1.readlines()
    data = []
    # Get input data
    for line in Lines:
        data.append(line.strip())
    return data

def main():
    """ Main entry point of the app """
    inputData = getInput()


    
    print('day 1 part 1:', maxCalories[0])
    print('day 1 part 2:', sum(maxCalories))
    return maxCalories

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()