from typing import List, Optional, Tuple, Dict
from collections import deque, defaultdict


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
        self.setup()
        print(self.broadast, self.flip, self.conj, self.val, self.Cin)

    def setup(self) -> int:
        self.val = {}
        self.Cin = defaultdict(list)

        def process(mapping):
            for key, outputs in mapping.items():
                self.val[key] = 0
                for n in outputs:
                    if n in self.conj:
                        self.Cin[n].append(key)

        process(self.flip)
        process(self.conj)

    def broadcast(self):
        signals = [(x, 0) for x in self.broadast]
        q = deque(signals)
        c = 0
        self.counts[0] += len(self.broadast)
        while q and c < 8:
            c += 1
            curr, signal = q.popleft()
            self.counts[signal] +=1  
            if curr in self.flip:
                if signal:
                    continue
                self.val[curr] = 1 if not self.val[curr] else 0
                s = [(x, self.val[curr]) for x in self.flip[curr]]
            elif curr in self.conj:
                self.val[curr] = 0 if all(self.val[x] for x in self.Cin[curr]) else 1
                s = [(x, self.val[curr]) for x in self.conj[curr]]
            q.extend(s)
            print(curr, self.val, q)
        print(q, self.val, s)

    def getTotal(self):
        total = 1
        self.counts = [0, 0]
        for _ in range(1):
            print()
            self.broadcast()
        print(self.counts)
        return total


if __name__ == "__main__":
    aplenty = Aplenty(True)
    print("Day 20 part 1:", aplenty.getTotal())
    # Total Runtime ~1.6s
