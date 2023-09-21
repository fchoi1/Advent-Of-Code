from typing import Optional, List


class Door:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(x.strip()) for x in file1.readlines()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.cardKey, self.doorKey = self.getInput()

    def transform(self, n: int, subjectNum: int) -> int:
        return (n * subjectNum) % 20201227

    def getKey(self) -> int:
        val = 7
        doorIndex = cardIndex = None
        index = 1
        while not doorIndex and not cardIndex:
            val = self.transform(val, 7)
            if val == self.cardKey:
                cardIndex = index
            if val == self.doorKey:
                doorIndex = index
            index += 1

        subject = val = self.cardKey if doorIndex else self.doorKey
        index = doorIndex if doorIndex else cardIndex

        for _ in range(index):
            val = self.transform(val, subject)
        return val


if __name__ == "__main__":
    door = Door()
    print("Day 25 part 1:", door.getKey())
    # Total Runtime  ~3.3s
