from typing import List, Optional, Tuple
from sympy import solve, Integer, symbols

class Hailstones:

    def getInput(self) -> List[Tuple[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        hailstones = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                pos, vel = line.split(" @ ")
                hailstones.append((tuple(map(int, pos.split(", "))), tuple(map(int, vel.split(", ")))))
            return hailstones

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.hailstones = self.getInput()

    def getCollisions(self) -> int:
        r = (7, 27) if self.useTest else (200_000_000_000_000, 400_000_000_000_000)
        count = 0
        for i, ((x1, y1, _), (vx1, vy1, _)) in enumerate(self.hailstones):
            for (x2, y2, _), (vx2, vy2, _) in self.hailstones[i + 1 :]:
                m1,m2= vy1 / vx1,vy2 / vx2
                b1, b2, = y1 - m1 * x1,y2 - m2 * x2
                if m2 != m1:
                    x = (b1 - b2) / (m2 - m1)
                    y = m1 * x + b1
                    past1 = x1 < x and vx1 < 0 or x1 > x and vx1 > 0
                    past2 = x2 < x and vx2 < 0 or x2 > x and vx2 > 0
                    if (
                        r[0] <= x <= r[1]
                        and r[0] <= y <= r[1]
                        and not past1
                        and not past2
                    ):
                        count += 1
        return count

    def findLine(self) -> int:
        xr, yr, zr, vxr, vyr, vzr = symbols("xr, yr, zr , vxr, vyr, vzr")
        eqs = []

        # x + vx * t = xr + vxr * t
        # t = (x - xr) / (vxr - vx) = (y - yr) / (vyr - vy) = (z - zr) / (vzr - vz)
        # 2 eqs - 6vars
        # need 2 more lines to solve 6 vars

        for (x, y, z), (vx, vy, vz) in self.hailstones[:3]:
            eqs.append((x - xr) * (vyr - vy) - (y - yr) * (vxr - vx))
            eqs.append((y - yr) * (vzr - vz) - (z - zr) * (vyr - vy))
        ans = [
            s for s in solve(eqs) if all(isinstance(n, Integer) for n in s.values())
        ][0]
        return ans[xr] + ans[yr] + ans[zr]


if __name__ == "__main__":
    hailstones = Hailstones()
    print("Day 24 part 1:", hailstones.getCollisions())
    print("Day 24 part 2:", hailstones.findLine())
