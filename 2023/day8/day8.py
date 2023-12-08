from typing import List, Optional, Tuple
from math import lcm


class Network:
    def getInput(self) -> Tuple[List[Tuple[str, int]], str]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        nodeMap = {}
        direction = ""
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                if not direction:
                    direction = line
                    continue
                if not line:
                    continue
                val, paths = line.split(" = ")
                left, right = paths[1:-1].split(", ")
                nodeMap[val] = (left, right)
            return nodeMap, direction

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.nodeMap, self.direction = self.getInput()

    def getSteps(self) -> int:
        steps = 0
        node = "AAA"
        while node != "ZZZ":
            currDir = self.direction[steps % len(self.direction)]
            node = self.nodeMap[node][0 if currDir == "L" else 1]
            steps += 1
        return steps

    def getSameSteps(self) -> int:
        steps = 0
        nodeList = []
        for key in self.nodeMap.keys():
            if key.endswith("A"):
                nodeList.append(key)
        nodeLoop = [None for _ in range(len(nodeList))]
        # Each start node only contains 1 node that ends w/ Z and each loop same dist from start
        while not all(n for n in nodeLoop):
            currDir = self.direction[steps % len(self.direction)]
            steps += 1
            for i in range(len(nodeList)):
                nodeList[i] = self.nodeMap[nodeList[i]][0 if currDir == "L" else 1]
                if nodeList[i].endswith("Z") and not nodeLoop[i]:
                    nodeLoop[i] = steps
        return lcm(*nodeLoop)


if __name__ == "__main__":
    network = Network()
    print("Day 8 part 1:", network.getSteps())
    print("Day 8 part 2:", network.getSameSteps())
