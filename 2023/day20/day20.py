from typing import List, Optional, Tuple, Dict


class Aplenty:
    def getInput(self) -> Tuple:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        broadcast = []
        flip = {}
        conj = {}
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                if line.startswith("broadcaster"):
                    broadcast = line.split(" -> ")[1].split(", ")
                    continue
                if line.startswith("%"):
                    split = line.split(" -> ")
                    flip[split[0][1:]] = split[1].split(", ")
                else:
                    split = line.split(" -> ")
                    conj[split[0][1:]] = split[1].split(", ")

            return broadcast, flip, conj

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.broadast, self.flip, self.conj = self.getInput()
        print(self.broadast, self.flip, self.conj)

    def getTotal(self) -> int:
        total = 0
        self.F = {}
        self.C = {}
        for key in self.flip.keys():
            self.F[key] = 0
        for key in self.conj.keys():
            self.C[key] = 0

        return total


if __name__ == "__main__":
    aplenty = Aplenty(True)
    print("Day 20 part 1:", aplenty.getTotal())
    # Total Runtime ~1.6s
