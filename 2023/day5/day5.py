from typing import List, Optional


class Seed:
    def getInput(self) -> List[List[List[int]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        seedMap, nextAttr = {}, {}
        attr = ""
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                if not line:
                    continue
                if "seeds:" in line:
                    seeds = [int(x) for x in line.split(": ")[1].split(" ")]
                    continue
                elif "-to-" in line:
                    start, _, attr = line.split()[0].split("-")
                    seedMap[attr] = []
                    nextAttr[start] = attr
                else:
                    start, dest, inc = [int(x) for x in line.split()]
                    seedMap[attr].append([start, dest, inc])
        return seedMap, nextAttr, seeds

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.seedMap, self.nextAttr, self.seeds = self.getInput()
        self.sortSeedMap()

    def sortSeedMap(self) -> None:
        for key in self.seedMap:
            self.seedMap[key].sort(key=lambda x: x[1])

    def getLowestSeed(self) -> int:
        lowest = float("inf")
        for val in self.seeds:
            attr = "seed"
            while attr != "location":
                attr = self.nextAttr[attr]
                for end, start, inc in self.seedMap[attr]:
                    if val >= start and val < start + inc:
                        val = val + (end - start)
                        break
            lowest = min(lowest, val)
        return lowest

    def getRanges(self) -> List[List[int]]:
        ranges = []
        for i, seedStart in enumerate(self.seeds[::2]):
            ranges.append([seedStart, seedStart + self.seeds[i * 2 + 1]])
        return ranges

    def getLowestSeedRange(self) -> int:
        ranges = self.getRanges()
        lowest = float("inf")
        for s, e in ranges:
            lowest = min(lowest, self.analyzeRange([[s, e - 1]], "soil"))
        return lowest

    def analyzeRange(self, ranges, attr) -> int:
        newRanges = []
        for end, start, inc in self.seedMap[attr]:
            temp = []
            while ranges:
                s, e = ranges.pop()
                before = [s, min(start, e)]
                overlap = [max(s, start), min(e, start + inc)]
                after = [max(start + inc, s), e]
                if before[1] > before[0]:
                    temp.append(before)
                if after[1] > after[0]:
                    temp.append(after)
                if overlap[1] > overlap[0]:
                    newRanges.append(
                        [overlap[0] + (end - start), overlap[1] + (end - start)]
                    )
            ranges = temp

        return min(newRanges)[0] if attr == "location" else  self.analyzeRange(newRanges + ranges, self.nextAttr[attr])


if __name__ == "__main__":
    seed = Seed()
    print("Day 5 part 1:", seed.getLowestSeed())
    print("Day 5 part 2:", seed.getLowestSeedRange())
