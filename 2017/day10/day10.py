from typing import List, Optional


class Knot:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [int(x) for x in file1.readline().strip().split(",")]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.lengths = self.getInput()
        self.length = 5 if useTest else 256
        self.hash = [i for i in range(self.length)]
        self.firstTwo = 0
        self.runLengths()
        print(self.lengths, self.hash)

    def reverseSubset(self, start: int, end: int):
        if end > self.length:
            end %= self.length
            tempHash = self.hash[start:] + self.hash[:end]
            tempHash.reverse()
            i = 0
            while start != end:
                self.hash[end], self.hash[start] = tempHash[i], tempHash[-i-1]
                print("reverse", tempHash, start, end, i, tempHash[i], tempHash[-1-i])
                i += 1
                end -= 1
                start += 1
                if end < 0:
                    end = self.length - 1
                if start >= self.length:
                    start = 0
        else:
            self.hash[start:end] = list(reversed(self.hash[start:end]))

    def runLengths(self) -> None:
        skip = 0
        index = 0
        for l in self.lengths:
            subset = index + l
            print(self.hash, index, subset)

            self.reverseSubset(index, subset)
            index = (index + subset + skip) % self.length
            skip += 1
        print("done", self.hash[0], self.hash[1], self.hash)
        self.firstTwo = self.hash[0] * self.hash[0]

    def getFirstTwo(self) -> int:
        return self.firstTwo


if __name__ == "__main__":
    knot = Knot(True)
    print("Day 10 part 1:", knot.getFirstTwo())
    # print("Day 10 part 2:", knot.getGarbage())
