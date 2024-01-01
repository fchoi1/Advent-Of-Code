from typing import Optional, Set, Dict
from collections import deque, defaultdict
from copy import deepcopy


class Snowverload:
    def getInput(self) -> Dict[str, Set[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        wires = defaultdict(set)
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                left, right = line.split(": ")
                right = right.split(" ")
                for node in right:
                    wires[node].add(left)
                    wires[left].add(node)
            return wires

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.wires = self.getInput()

    def findPath(self, g: Dict[str, Set[str]], start: str, end: str) -> Dict[str, str]:
        q = deque([start])
        parent = {}
        seen = set()
        while q:
            node = q.popleft()
            if node == end:
                return parent
            for n in g[node]:
                if n not in seen:
                    seen.add(n)
                    q.append(n)
                    parent[n] = node
        return parent

    def bfs(self, g: Dict[str, Set[str]], node: str) -> Set[str]:
        q = deque([node])
        seen = set()
        while q:
            node = q.popleft()
            if node in seen:
                continue
            seen.add(node)
            for n in g[node]:
                q.append(n)
        return seen

    def getTotal(self) -> int:
        nodes = list(self.wires)
        start = nodes[0]
        for end in nodes[1:]:
            copy = deepcopy(self.wires)
            for _ in range(3):
                parent = self.findPath(copy, start, end)
                node = end
                # delete path 3 times
                while node != start:
                    copy[node].remove(parent[node])
                    copy[parent[node]].remove(node)
                    node = parent[node]
            seen = self.bfs(copy, node)
            if len(seen) != len(self.wires):
                return len(seen) * (len(self.wires) - len(seen))
        return -1


if __name__ == "__main__":
    snowverload = Snowverload()
    print("Day 25 part 1:", snowverload.getTotal())
