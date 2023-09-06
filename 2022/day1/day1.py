from typing import List, Optional


class Calories:
    def getInput(self) -> List[str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                data.append(line.strip())
            return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.input = self.getInput()
        
    def getMax(self, num: Optional[int] = 1) -> int:
        maxCalories = [float("-inf")] * num
        currentCal = 0
        for data in self.input:
            if data:
                currentCal += int(data)
            else:
                if currentCal >= maxCalories[num-1]:
                    maxCalories[num-1] = currentCal
                    maxCalories = sorted(maxCalories, reverse=True)
                currentCal = 0

        return sum(maxCalories[:num])


if __name__ == "__main__":
    calories = Calories()
    print("Day 1 part 1:", calories.getMax())
    print("Day 1 part 2:", calories.getMax(3))
