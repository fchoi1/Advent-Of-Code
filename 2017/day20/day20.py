from typing import Optional, List, Dict
import re


class Particle:
    def __init__(self, pos: List[int], vel: List[int], acc: List[int]) -> None:
        self.pos, self.vel, self.acc = pos, vel, acc
        self.prev = None

    def update(self) -> None:
        self.prev = self.pos
        for i in range(3):
            self.vel[i] += self.acc[i]
            self.pos[i] += self.vel[i]


class GPU:
    def getInput(self) -> Dict[int, Particle]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        particles = {}
        delimiters = "|".join(map(re.escape, ["=<", ">,", ">"]))
        with open(inputFile, "r") as file1:
            for i, line in enumerate(file1):
                string = re.split(delimiters, line.strip())
                pos = list(map(int, string[1].split(",")))
                vel = list(map(int, string[3].split(",")))
                acc = list(map(int, string[5].split(",")))
                particles[i] = Particle(pos, vel, acc)
        return particles

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.particles = self.getInput()

    def getClosest(self) -> int:
        minAcc = float("inf")
        minKey = None
        for key, particle in self.particles.items():
            if sum(map(abs, particle.acc)) < minAcc:
                minAcc = sum(map(abs, particle.acc))
                minKey = key
        return minKey

    def getParticlesLeft(self) -> int:
        loop = 100  # random large loop

        for _ in range(loop):
            toRemove, seen = set(), {}
            for key, particle in self.particles.items():
                particle.update()
                posKey = tuple(particle.pos)
                if posKey in seen:
                    toRemove.add(key)
                    if seen[posKey] not in toRemove:
                        toRemove.add(seen[posKey])
                    continue
                seen[posKey] = key
            for key in toRemove:
                del self.particles[key]
        return len(self.particles)


if __name__ == "__main__":
    gpu = GPU()
    print("Day 20 part 1:", gpu.getClosest())
    print("Day 20 part 2:", gpu.getParticlesLeft())
