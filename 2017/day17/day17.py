from typing import Optional


class Node:
    def __init__(self, val: int) -> None:
        self.val = val
        self.next = None


class Spinlock:
    def getInput(self) -> int:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return int(file1.readline().strip())

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.step = self.getInput()

    def getPosition(self) -> int:
        node = Node(0)
        node.next = node
        for i in range(1, 2018):
            for _ in range(self.step):
                node = node.next
            newNode = Node(i)
            node.next, newNode.next = newNode, node.next
            node = newNode
        return node.next.val

    def getPosition2(self) -> int:
        pos1Val = currPos = 0
        for i in range(1, 50_000_000):
            currPos = ((currPos + self.step) % i + 1) % (i + 1)
            if currPos == 1:
                pos1Val = i
        return pos1Val


if __name__ == "__main__":
    spinlock = Spinlock()
    print("Day 17 part 1:", spinlock.getPosition())
    print("Day 17 part 2:", spinlock.getPosition2())
    # Total Runtime ~6.15s
