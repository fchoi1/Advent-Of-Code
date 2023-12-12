from typing import List, Optional, Tuple


class Springs:
    def getInput(self) -> List[Tuple[str, List[int]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        row = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip().split()
                row.append((line[0], [int(x) for x in line[1].split(",")]))
            return row

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.lines = self.getInput()

    def getTotal(self, isPart2: Optional[bool] = False) -> int:
        total = 0
        for row, counts in self.lines[:]:
            if isPart2:
                row = "?".join([row] * 5)
                counts = counts * 5
            total += self.countValid(row, counts, 0, 0, 0, {})
        return total

    def countValid(self, row, counts, i, ci, hashes, seen) -> int:
        key = (i, ci, hashes)
        if key in seen:
            return seen[key]
        if i == len(row):
            return int(
                (ci == len(counts) and hashes == 0)
                or (ci == len(counts) - 1 and hashes == counts[ci])
            )
        #  Slight Optimization
        if ci < len(counts) and hashes > counts[ci]:
            return 0
        ans = 0
        if row[i] in ".?":
            # continue as a .
            if hashes == 0:
                ans += self.countValid(row, counts, i + 1, ci, hashes, seen)
            # when hash lenght is met
            if hashes > 0 and ci < len(counts) and counts[ci] == hashes:
                ans += self.countValid(row, counts, i + 1, ci + 1, 0, seen)

        if row[i] in "#?":
            ans += self.countValid(row, counts, i + 1, ci, hashes + 1, seen)
        seen[key] = ans
        return ans


if __name__ == "__main__":
    springs = Springs()
    print("Day 12 part 1:", springs.getTotal())
    print("Day 12 part 2:", springs.getTotal(True))
