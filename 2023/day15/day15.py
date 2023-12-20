from typing import List, Optional


class Library:
    def getInput(self) -> List[str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return file1.readline().strip().split(",")

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.data = self.getInput()

    def getHash(self, string) -> int:
        hashValue = 0
        for char in string:
            hashValue = ((hashValue + ord(char)) * 17) % 256
        return hashValue

    def getHashSum(self) -> int:
        return sum(self.getHash(line) for line in self.data)

    def getTotal(self) -> int:
        total = 0
        boxes = [{"list": []} for _ in range(256)]
        for line in self.data:
            label, val = line.split("=") if "=" in line else line.split("-")
            currBox = boxes[self.getHash(label)]

            if val:
                if label in currBox:
                    index = currBox[label]
                    currBox["list"][index] = int(val)
                else:
                    currBox[label] = len(currBox["list"])
                    currBox["list"].append(int(val))
            elif label in currBox:
                index = currBox[label]
                currBox["list"][index] = 0
                del currBox[label]

        for i, box in enumerate(boxes):
            rank = 0
            for val in box["list"]:
                if val == 0:
                    continue
                rank += 1
                total += val * rank * (i + 1)
        return total


if __name__ == "__main__":
    library = Library()
    print("Day 15 part 1:", library.getHashSum())
    print("Day 15 part 2:", library.getTotal())
