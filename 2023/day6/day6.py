from typing import List, Optional, Tuple


class Race:
    def getInput(self) -> Tuple[List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            times = list(map(int, file1.readline().split()[1:]))
            dist = list(map(int, file1.readline().split()[1:]))
        return times, dist

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.times, self.dist = self.getInput()

    def getTotal(self) -> int:
        total = 1
        for d, t in zip(self.dist, self.times):
            total *= sum(s * (t - s) > d for s in range(t))
        return total

    def getLongerRace(self) -> int:
        totalTime = int("".join(map(str, self.times)))
        totalDist = int("".join(map(str, self.dist)))
        return sum(s * (totalTime - s) > totalDist for s in range(totalTime))


if __name__ == "__main__":
    race = Race()
    print("Day 6 part 1:", race.getTotal())
    print("Day 6 part 2:", race.getLongerRace())
    # Total Runtime ~2.89s
