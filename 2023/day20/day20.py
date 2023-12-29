from typing import Optional, Tuple
from collections import deque, defaultdict
from math import lcm


class Pulse:
    def getInput(self) -> Tuple:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        broadcast = []
        flip, conj = {}, {}
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

    def reset(self) -> None:
        self.val = {}
        self.Cin = defaultdict(list)
        for key, outputs in [*self.conj.items(), *self.flip.items()]:
            self.val[key] = 0
            for n in outputs:
                if n in self.conj:
                    self.Cin[n].append(key)

    def broadcast(
        self,
        feed: Optional[str] = "",
        presses: Optional[int] = 0,
    ) -> None:
        signals = [(x, 0) for x in self.broadast]
        q = deque(signals)
        self.counts[0] += 1
        output = "output" if self.useTest else "rx"
        while q:
            curr, signal = q.popleft()
            self.counts[signal] += 1
            if curr == output:
                continue
            if curr in self.flip:
                if signal:
                    continue
                self.val[curr] = 1 if not self.val[curr] else 0
                s = [(x, self.val[curr]) for x in self.flip[curr]]
            elif curr in self.conj:
                self.val[curr] = 0 if all(self.val[x] for x in self.Cin[curr]) else 1
                if feed and feed in self.conj[curr] and self.val[curr]:
                    self.cycles[curr] = presses
                s = [(x, self.val[curr]) for x in self.conj[curr]]
            q.extend(s)

    def getTotal(self) -> int:
        self.reset()
        self.counts = [0, 0]
        for _ in range(1000):
            self.broadcast()
        return self.counts[0] * self.counts[1]

    def getButtonPress(self) -> int:
        self.reset()
        # Assumed feed is a conjunction
        for key, outputs in self.conj.items():
            if "rx" in outputs:
                feed = key
                break
        self.cycles = {name: None for name in self.Cin[feed]}
        counter = 0
        while True:
            counter += 1
            self.broadcast(feed, counter)
            if all(self.cycles[key] for key in self.Cin[feed]):
                break
        return lcm(*self.cycles.values())


if __name__ == "__main__":
    pulse = Pulse()
    print("Day 20 part 1:", pulse.getTotal())
    print("Day 20 part 2:", pulse.getButtonPress())
