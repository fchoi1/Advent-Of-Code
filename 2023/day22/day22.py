from typing import List, Optional, Tuple


class Bricks:
    def getInput(self) -> List[Tuple[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        ends = []
        with open(inputFile, "r") as file1:
            for line in file1:
                a, b = map(
                    lambda x: tuple(map(int, x.split(","))), line.strip().split("~")
                )
                ends.append((a, b))
            return ends

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.bars = self.getInput()
        self.bars.sort(key=lambda x: x[0][2])
        self.supports = []
        self.removable = set()
        self.fall = 0
        self.drop()

    def drop(self) -> None:
        tallest = self.bars[-1][1][2]
        layers = [{} for _ in range(tallest + 1)]
        for i, brick in enumerate(self.bars[:]):
            start, end = brick
            stable = False
            z = start[2]
            while not stable and z >= 0:
                layer = layers[z]
                supported = [set(), set()]
                if start[2] == end[2]:
                    if start[0] == end[0]:
                        s, e, axis = start[1], end[1] + 1, start[0]
                    else:
                        s, e, axis = start[0], end[0] + 1, start[1]

                    for val in range(s, e):
                        coord = (axis, val) if start[0] == end[0] else (val, axis)
                        if coord in layer:
                            stable = True
                            supported[0].add(layer[coord])
                            self.supports[layer[coord]][1].add(i)

                    if stable or z == 0:
                        for val in range(s, e):
                            coord = (axis, val) if start[0] == end[0] else (val, axis)
                            layers[z + 1][coord] = i
                else:
                    if (start[0], start[1]) in layer or z == 0:
                        stable = True
                        newTop = z + 1 + (end[2] - start[2])
                        layers[newTop][(start[0], start[1])] = i
                        if (start[0], start[1]) in layer:
                            supported = [set([layer[(start[0], start[1])]]), set()]
                            self.supports[layer[(start[0], start[1])]][1].add(i)
                z -= 1
            self.supports.append(supported)

        for i, (_, s) in enumerate(self.supports):
            if all(len(self.supports[i][0]) > 1 for i in s) or len(s) == 0:
                self.removable.add(i)
            else:
                moved = set([i])
                self.countFall(i, moved)
                self.fall += len(moved) - 1

    def countFall(self, i, moved):
        _, s = self.supports[i]
        for base in s:
            if all(x in moved for x in self.supports[base][0]):
                moved.add(base)
                self.countFall(base, moved)

    def getRemovable(self) -> int:
        return len(self.removable)

    def countRemovable(self) -> int:
        return self.fall


if __name__ == "__main__":
    bricks = Bricks()
    print("Day 22 part 1:", bricks.getRemovable())
    print("Day 22 part 2:", bricks.countRemovable())
