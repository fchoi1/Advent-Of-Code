from typing import List, Optional, Dict
from collections import Counter


class Node:
    def __init__(self, name: str, val: Optional[int] = 0) -> None:
        self.name = name
        self.val = val
        self.children = {}

    def addChildren(self, node: "Node") -> None:
        self.children[node.name] = node


class Circus:
    def getInput(self) -> Dict[str, Node]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        nodeMap = {}
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                strings = line.strip().split(" -> ")
                parentInfo = strings[0].split(" ")
                parentNode = parentInfo[0]
                val = int(parentInfo[1][1:-1])
                if parentNode in nodeMap:
                    nodeMap[parentNode].val = val
                else:
                    nodeMap[parentNode] = Node(parentNode, val)
                if len(strings) < 2:
                    continue
                for node in strings[1].split(", "):
                    if node not in nodeMap:
                        child = Node(node)
                        nodeMap[node] = child
                    nodeMap[parentNode].addChildren(nodeMap[node])
        return nodeMap

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.nodeMap = self.getInput()
        self.root = self.getRoot()
        self.diff = 0

    def getWieght(self, currNode: Node) -> int:
        if not currNode.children:
            return currNode.val
        totalWeight = 0
        for node in currNode.children.values():
            totalWeight += self.getWieght(node)
        return currNode.val + totalWeight

    def checkWieghts(self, currNode: Node, found: Optional[bool] = False) -> None:
        if not currNode.children:
            return
        weights = []
        for node in currNode.children.values():
            weights.append((self.getWieght(node), node))
        counts = Counter(item[0] for item in weights)
        if len(counts) > 1:
            unique = next((item for item in weights if counts[item[0]] == 1), None)
            commonVal = next((item[0] for item in weights if counts[item[0]] > 1), None)
            self.diff = unique[1].val - (unique[0] - commonVal)
            self.checkWieghts(unique[1], True)
            return
        if found:
            return
        for node in currNode.children.values():
            self.checkWieghts(node)

    def getRoot(self) -> str:
        seen = set()
        for node in self.nodeMap.values():
            if not node.children:
                seen.add(node.name)
            for node in node.children.values():
                seen.add(node.name)
        for node in self.nodeMap.values():
            if node.name not in seen:
                return node.name
        return ""

    def getRootName(self) -> str:
        return self.root

    def getCorrectWeight(self) -> int:
        self.checkWieghts(self.nodeMap[self.root])
        return self.diff


if __name__ == "__main__":
    circus = Circus()
    print("Day 7 part 1:", circus.getRoot())
    print("Day 7 part 2:", circus.getCorrectWeight())
