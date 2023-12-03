from typing import Optional, List, Tuple


class Cubes:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [list(x.strip()) for x in file1]

    def __init__(self, useTest: Optional[bool] = False, rounds: Optional[int] = 6) -> None:
        self.useTest = useTest
        self.cubeFace = self.getInput()
        self.rounds = rounds
        self.reset()

    def reset(self, use4D: Optional[bool] = False) -> int:
        self.cubes = self.getStartingCubes(use4D)
        self.dirs = self.getDirections(use4D)

    def getStartingCubes(self, use4D: bool) -> set:
        if use4D:
            return {(x, y, 0, 0) for y, row in enumerate(self.cubeFace) for x, val in enumerate(row) if val == "#"}
        else:
            return {(x, y, 0) for y, row in enumerate(self.cubeFace) for x, val in enumerate(row) if val == "#"}

    def getDirections(self, use4D: bool) -> List:
        directions = [(x, y, z) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)]
        if use4D:
            directions = [(x, y, z, w) for (x, y, z) in directions for w in range(-1, 2)]
            directions.remove((0, 0, 0, 0))
        else:
            directions.remove((0, 0, 0))
        return directions

    def checkActive(self, cube: Tuple[int], cubeSet: set) -> bool:
        count = 0
        isActive = cube in self.cubes

        for direction in self.dirs:
            neighbor = tuple(coord + d for coord, d in zip(cube, direction))
            if neighbor in self.cubes:
                count += 1
        if count == 3 and not isActive:
            cubeSet.add(cube)
        if count in [2, 3] and isActive:
            cubeSet.add(cube)
        return cubeSet

    def getDimensions(self) -> List[Tuple[int]]:
        max_values = [max(coord) for coord in zip(*self.cubes)]
        min_values = [min(coord) for coord in zip(*self.cubes)]
        max_values = [value + 2 for value in max_values]
        min_values = [value - 1 for value in min_values]
        return [(minVal, maxVal) for minVal, maxVal in zip(min_values, max_values)]

    def getActiveCubes(self, use4D: Optional[bool] = False) -> int:
        self.reset(use4D)
        for _ in range(self.rounds):
            cubeSet = set()
            dimensions = self.getDimensions()
            for cube in self.generateCubes(dimensions, use4D):
                cubeSet = self.checkActive(cube, cubeSet)
            self.cubes = cubeSet
        return len(self.cubes)

    def generateCubes(self, dimensions: List[Tuple[int]], use4D: bool) -> List[Tuple[int]]:
        if use4D:
            for x in range(*dimensions[0]):
                for y in range(*dimensions[1]):
                    for z in range(*dimensions[2]):
                        for w in range(*dimensions[3]):
                            yield (x, y, z, w)
        else:
            for x in range(*dimensions[0]):
                for y in range(*dimensions[1]):
                    for z in range(*dimensions[2]):
                        yield (x, y, z)


if __name__ == "__main__":
    cubes = Cubes()
    print("Day 17 part 1:", cubes.getActiveCubes())
    print("Day 17 part 2:", cubes.getActiveCubes(True))
    # Total Runtime 3.9s
