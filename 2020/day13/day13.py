from typing import Optional, Tuple
import math


# Extended Euclidean Algorithm,
# Ref:  https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


class Shuttle:
    def getInput(self) -> Tuple:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            lines = file1.readlines()
            timestamp = int(lines[0])
            times = [int(x) if x != "x" else 0 for x in lines[1].split(",")]
            return (timestamp, times)

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.timestamp, self.times = self.getInput()

    def getClosest(self) -> int:
        closest = float("inf")
        closestBus = 0
        for bus in self.times:
            if bus:
                diff = bus - self.timestamp % bus
                if diff < closest:
                    closestBus = bus
                    closest = diff

        return closest * closestBus

    def getEarliestTimestampe(self) -> int:
        currLcm = 1
        intersection = prev = 0
        for i, bus in enumerate(self.times):
            if bus:
                intersection = self.getOffsetPhase(bus, currLcm, (intersection + i - prev))
                prev = i
                currLcm = math.lcm(currLcm, bus)
        return intersection - i

    def getOffsetPhase(self, x: int, y: int, offset: int) -> int:
        gcd, s, t = extended_gcd(x, y)
        period = (x * y) // gcd
        phase_difference = -(-offset % y)
        phase = (s * phase_difference // gcd * x) % period
        return int(phase)


if __name__ == "__main__":
    shuttle = Shuttle()
    print("Day 13 part 1:", shuttle.getClosest())
    print("Day 13 part 2:", shuttle.getEarliestTimestampe())
