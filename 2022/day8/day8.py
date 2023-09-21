from typing import List, Dict, Any, Optional


class Trees:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x.strip() for x in file1.readlines()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.inputData = self.getInput()
        self.trees = []
        self.numVisible = 0
        self.size = [0, 0]  #  [row, col]
        self.maxScenicScore = 0
        self.generateGrid()

    def generateGrid(self) -> None:
        for row in self.inputData:
            self.trees.append([int(x) for x in row])

        self.size[0] = len(self.trees)
        self.size[1] = len(self.trees[0])

    def getTreeProps(self, index: int, row: List[int]) -> Dict[str, Any]:
        left = right = index
        leftVisible = rightVisible = True
        leftScore = rightScore = 0

        while left > 0:
            left -= 1
            leftScore += 1
            if row[index] <= row[left]:
                leftVisible = False
                break

        while right < len(row) - 1:
            right += 1
            rightScore += 1
            if row[index] <= row[right]:
                rightVisible = False
                break

        return {
            "scenicScore": leftScore * rightScore,
            "isVisible": (leftVisible or rightVisible),
        }

    def calculateNumVisible(self) -> None:
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                treeRowProps = self.getTreeProps(i, [row[j] for row in self.trees])
                treeColProps = self.getTreeProps(j, self.trees[i])
                scenicScore = treeColProps["scenicScore"] * treeRowProps["scenicScore"]
                if treeRowProps["isVisible"] or treeColProps["isVisible"]:
                    self.numVisible += 1
                if scenicScore > self.maxScenicScore:
                    self.maxScenicScore = scenicScore

    def getNumVisible(self) -> int:
        return self.numVisible

    def getScenicScore(self) -> int:
        return self.maxScenicScore


if __name__ == "__main__":
    tree = Trees()
    tree.calculateNumVisible()
    print("Day 8 part 1:", tree.getNumVisible())
    print("Day 8 part 2:", tree.getScenicScore())
