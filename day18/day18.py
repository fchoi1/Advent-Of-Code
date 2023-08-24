from typing import List, Optional, Union, Tuple
from collections import deque


class Lava:
    def getInput(self) -> List[List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            Lines = file1.readlines()
            cubes = []
            for line in Lines:
                line = line.strip()
                cubes.append(list(map(int, line.split(","))))
        return cubes

    def __init__(self, useTest: Optional[bool] = False) -> None:
        """Main entry point of the app"""
        self.useTest = useTest
        self.cubes = self.getInput()
        self.max = self.getMaxDimensions()

        self.seen = set()
        self.surfaceArea = 0

    def updateArea(self, cube: List[int]) -> None:
        [cubeX, cubeY, cubeZ] = cube
        directions = [
            [1, 0, 0],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0],
            [0, 0, 1],
            [0, 0, -1],
        ]

        for dx, dy, dz in directions:
            key = f"{cubeX + dx},{cubeY + dy},{cubeZ + dz}"
            if key in self.seen:
                self.surfaceArea -= 2

    def getSurfaceArea(self) -> int:
        for [x, y, z] in self.cubes:
            key = f"{x},{y},{z}"
            if key not in self.seen:
                self.seen.add(key)
                self.surfaceArea += 6
                self.updateArea([x, y, z])
        return self.surfaceArea

    def getMaxDimensions(self) -> List[int]:
        maxX = max(item[0] for item in self.cubes)
        maxY = max(item[1] for item in self.cubes)
        maxZ = max(item[2] for item in self.cubes)
        return [maxX + 1, maxY + 1, maxZ + 1]

    def surfaceAreaNoPockets(self) -> int:
        self.visited = self.seen.copy()

        for x in range(1, self.max[0]):
            for y in range(1, self.max[1]):
                for z in range(1, self.max[2]):
                    key = f"{x},{y},{z}"
                    if key not in self.visited:
                        [isPocket, subtractArea] = self.bfs([x, y, z], 0)

                        if isPocket:
                            self.surfaceArea -= subtractArea
        return self.surfaceArea

    def bfs(self, currentCoord: List[int], subtract: int) -> Tuple[Union[bool, int]]:
        q = deque([tuple(currentCoord)])
        isPocket = True
        subtract = 0
        while q:
            current = q.popleft()
            if current in self.visited:
                continue

            self.visited.add(current)
            directions = [
                [1, 0, 0],
                [-1, 0, 0],
                [0, 1, 0],
                [0, -1, 0],
                [0, 0, 1],
                [0, 0, -1],
            ]
            [currX, currY, currZ] = current

            for dx, dy, dz in directions:
                key = f"{currX + dx},{currY + dy},{currZ + dz}"
                newCoords = (currX + dx, currY + dy, currZ + dz)

                if not self.inBounds(newCoords):
                    isPocket = False
                    continue

                if key in self.seen:  # touching solid face
                    subtract += 1
                else:
                    q.append(newCoords)
        return (isPocket, subtract)

    def inBounds(self, coords: List[int]) -> bool:
        [currX, currY, currZ] = coords
        currentKey = f"{currX},{currY},{currZ}"
        if currentKey in self.seen:
            return True
        return (
            1 < currX < self.max[0]
            and 1 < currY < self.max[1]
            and 1 < currZ < self.max[2]
        )


if __name__ == "__main__":
    """This is executed when run from the command line"""
    lava = Lava(False)
    print("Day 18 part 1:", lava.getSurfaceArea())
    print("Day 18 part 2:", lava.surfaceAreaNoPockets())
