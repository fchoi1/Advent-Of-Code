from typing import Optional, List


class Adapter:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return set([int(x.strip()) for x in file1])

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.adapter = self.getInput()
        self.target = max(self.adapter)
        self.adapter.add(0)  #  add  starting
        self.visited = {}

    def getDiff(self) -> int:
        curr = 0
        adapterCount = [1, 0, 1]

        while curr < self.target:
            for i in range(1, 4):
                if (curr + i) in self.adapter:
                    adapterCount[i - 1] += 1
                    curr += i
                    break
        return adapterCount[0] * (adapterCount[2])

    # DP Solution
    def findValidPathsDP(self) -> int:
        curr = min(self.adapter)
        paths = {curr: 1}
        while curr < self.target:
            for i in range(1, 4):
                if (curr + i) in self.adapter:
                    numPaths = 0
                    for j in range(1, 4):
                        if (curr + i - j) in self.adapter:
                            numPaths += paths[curr + i - j]
                    paths[(curr + i)] = numPaths
                    curr += i
                    break
        return paths[self.target]

    # DFS Solution
    def findValidPathsDFS(self, num: int) -> int:
        if num in self.visited:
            return self.visited[num]

        if num >= self.target:
            return 1

        total = sum(
            self.findValidPathsDFS(num + i)
            for i in range(1, 4)
            if (num + i) in self.adapter
        )

        self.visited[num] = total
        return total

    def getArrangement(self) -> int:
        print("findValidPaths With DP", self.findValidPathsDP())
        return self.findValidPathsDFS(min(self.adapter))


if __name__ == "__main__":
    adapter = Adapter()
    print("Day 10 part 1:", adapter.getDiff())
    print("Day 10 part 2:", adapter.getArrangement())
