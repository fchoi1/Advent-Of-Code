from typing import List, Optional, Tuple


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Grove:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
            return [int(item.strip()) for item in Lines]

    def __init__(
        self, useTest: Optional[bool] = False, decrypt: Optional[int] = 811589153
    ) -> None:
        """Main entry point of the app"""
        self.useTest = useTest
        self.mapFile = self.getInput()
        self.length = len(self.mapFile)
        self.decryption = decrypt

    # For Debugging
    def printList(self, node: Node) -> None:
        arr = []
        nextNode = node
        while nextNode != node.left:
            arr.append(nextNode.val)
            nextNode = nextNode.right
        arr.append(nextNode.val)
        print(arr)

    def applyDecryption(self, mapFile: List[int]) -> List[int]:
        return [self.decryption * val for val in mapFile]

    # Doubly Linked List is faster than single Linked  List
    def createLinkedList(self, mapFile: List[int]) -> List[Node]:
        nodeList = [Node(mapFile[0])]
        head = prev = nodeList[0]
        for num in mapFile[1:]:
            newNode = Node(num)
            prev.right = newNode
            newNode.left = prev
            prev = newNode
            nodeList.append(newNode)

        prev.right = head
        head.left = prev
        return nodeList

    def mixFile(self, nodeList: List[Node]) -> Tuple[Node | List[Node]]:
        zeroNode = None

        for node in nodeList:
            if node.val == 0:
                zeroNode = node
                continue
            steps = node.val % (self.length - 1)

            if steps == 0:
                continue
            target = node
            for _ in range(steps):
                target = target.right

            # insert and deleting  link
            node.left.right = node.right
            node.right.left = node.left

            target.right.left = node
            node.right = target.right

            target.right = node
            node.left = target

        return (zeroNode, nodeList)

    # at  most the order gets moved once or not, somehow track position on input
    def getCoods(self, applyDecrypt: bool) -> int:
        mapFile = self.applyDecryption(self.mapFile) if applyDecrypt else self.mapFile
        loops = 10 if applyDecrypt else 1

        nodeList = self.createLinkedList(mapFile)
        for _ in range(loops):
            zeroNode, nodeList = self.mixFile(nodeList)

        node = zeroNode
        coords = 0
        for _ in range(3):
            for _ in range(1000):
                node = node.right
            coords += node.val
        return coords


if __name__ == "__main__":
    """This is executed when run from the command line"""
    grove = Grove(False)
    print("Day 20 part 1:", grove.getCoods(False))
    print("Day 20 part 2:", grove.getCoods(True))
    # Total Runtime ~ 3.5 Seconds
