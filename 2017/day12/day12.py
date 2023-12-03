from typing import Optional, Set, Dict
from collections import defaultdict


class Plumber:
    def getInput(self) -> Dict[int, Set[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        pipeMap = defaultdict(set)
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip().split(" <-> ")
                for end in line[1].split(","):
                    pipeMap[int(line[0])].add(int(end))
        return pipeMap

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.pipeMap = self.getInput()
        self.count = self.groupCount = 0

    def countID(self, pipeID: int, visited: Set[int]) -> None:
        if pipeID in visited:
            return
        visited.add(pipeID)
        self.count += 1
        for pipe in self.pipeMap[pipeID]:
            self.countID(pipe, visited)

    def getCount(self) -> int:
        self.count = 0
        self.countID(0, set())
        return self.count

    def getGroups(self) -> int:
        visited = set()
        for pipeID in self.pipeMap.keys():
            if pipeID not in visited:
                self.groupCount += 1
                self.countID(pipeID, visited)
        return self.groupCount


if __name__ == "__main__":
    plumber = Plumber(True)
    print("Day 12 part 1:", plumber.getCount())
    print("Day 12 part 2:", plumber.getGroups())
