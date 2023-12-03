from typing import Optional, List, Dict, Set
from collections import defaultdict


class Moat:
    def getInput(self) -> List[List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        bridges = defaultdict(set)
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip().split("/")
                bridges[int(line[0])].add(int(line[1]))
                bridges[int(line[1])].add(int(line[0]))
        return bridges

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.bridges = self.getInput()
        self.strongest = self.strongestLongest = self.Longest = 0
        self.seen = set()
        self.dfs(0, 0, [], self.bridges)

    def generateKey(self, bList: List[List[int]]) -> str:
        bList.sort(key=lambda x: (x[0], x[1]))
        key = ""
        for pair in bList:
            key += f"{str(pair[0])}/{str(pair[1])}-"
        return key

    def dfs(
        self,
        end: int,
        strength: int,
        bList: List[List[int]],
        bridges: Dict[int, Set[int]],
    ) -> None:
        key = self.generateKey(bList)
        if key in self.seen:
            return
        self.seen.add(key)
        if len(bridges[end]) == 0:
            self.strongest = max(self.strongest, strength)
            if len(bList) >= self.Longest:
                self.Longest = len(bList)
                self.strongestLongest = max(self.strongestLongest, strength)
            return

        for link in bridges[end].copy():
            bList.append([min(end, link), max(end, link)])
            bridges[link].discard(end)
            bridges[end].discard(link)
            self.dfs(link, strength + end + link, bList, bridges)
            bridges[link].add(end)
            bridges[end].add(link)
            bList.pop()

    def getStrongest(self) -> int:
        return self.strongest

    def getStrongestLongest(self) -> int:
        return self.strongestLongest


if __name__ == "__main__":
    moat = Moat()
    print("Day 24 part 1:", moat.getStrongest())
    print("Day 24 part 2:", moat.getStrongestLongest())
