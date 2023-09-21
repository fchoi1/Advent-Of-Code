from typing import Optional, List, Dict, Set


class Allergen:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        allergensList = []
        with open(inputFile, "r") as file1:
            for line in file1:
                ingredients, allergens = (
                    set(line.strip().split(" (contains ")[0].split()),
                    set(line.strip().split(" (contains ")[1].replace(")", "").split(", ")),
                )
                allergensList.append((ingredients, allergens))
        return allergensList

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.allergensList = self.getInput()
        self.allergenItems = {}

    def checkAllergens(self) -> None:
        seenAllergens = set()
        while True:
            allergenDict = {}
            for items, allergens in self.allergensList:
                updatedItems = set(item for item in items if item not in self.allergenItems)
                for allergen in allergens - seenAllergens:
                    if allergen not in allergenDict:
                        allergenDict[allergen] = updatedItems
                    else:
                        allergenDict[allergen] = allergenDict[allergen] & updatedItems
            isUpdated = False
            for allergen, items in allergenDict.items():
                if len(items) == 1:
                    item = items.pop()
                    self.allergenItems[item] = allergen
                    seenAllergens.add(allergen)
                    isUpdated = True
            if not isUpdated:
                break

    def getHealthyIngredients(self) -> int:
        self.checkAllergens()
        return sum(1 for items, _ in self.allergensList for item in items if item not in self.allergenItems)

    def getCanonicalItems(self) -> str:
        return ",".join(sorted(self.allergenItems, key=lambda k: self.allergenItems[k]))


if __name__ == "__main__":
    allergen = Allergen()
    print("Day 21 part 1:", allergen.getHealthyIngredients())
    print("Day 21 part 2:", allergen.getCanonicalItems())
