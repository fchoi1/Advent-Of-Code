from typing import Optional, Dict, List, Set
import re


class Haversacks:
    def getInput(self) -> Dict[int, List[str]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            data = {}
            delimiters = "|".join(map(re.escape, [" bags contain ", " ", ", ", "."]))
            for line in file1.readlines():
                line = line.strip().replace(" bags", "").replace(" bag", "")
                splited = re.split(delimiters, line)
                connections = []
                if splited[3] == "no":
                    continue
                for i in range(3, 3 + len(splited[4:]), 3):
                    connections.append((int(splited[i]), splited[i + 1] + splited[i + 2]))
                data["".join(splited[:2])] = connections
            return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.bags = self.getInput()
        self.target = "shinygold"

    def hasTarget(self, bag: str, visited: Set) -> bool:
        if bag not in self.bags or bag in visited:
            return False

        if bag == self.target:
            return True

        visited.add(bag)

        total = []
        for _, nextBag in self.bags[bag]:
            total.append(self.hasTarget(nextBag, visited))

        return any(n for n in total)

    def getBagsWithTarget(self) -> int:
        count = 0
        for bag in self.bags:
            if self.hasTarget(bag, set()) and bag != self.target:
                count += 1
        return count

    def getBagsInTarget(self) -> int:
        return self.getNumBags(self.target, {})

    def getNumBags(self, bag: str, bagDict: Dict) -> int:
        if bag not in self.bags:
            return 0

        if bag in bagDict:
            return bagDict[bag]

        total = 0
        for num, nextBag in self.bags[bag]:
            total += num + num * self.getNumBags(nextBag, bagDict)

        bagDict[bag] = total
        return total


if __name__ == "__main__":
    haversacks = Haversacks()
    print("Day 7 part 1:", haversacks.getBagsWithTarget())
    print("Day 7 part 2:", haversacks.getBagsInTarget())
