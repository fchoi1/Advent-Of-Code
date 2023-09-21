from typing import Optional, List, Tuple, Set


class Lobby:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [x.strip() for x in file1.readlines()]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.lineList = self.getInput()
        self.dirMap = {
            "ne": [1, -1, 0],
            "sw": [-1, 1, 0],
            "nw": [0, -1, 1],
            "se": [0, 1, -1],
            "e": [1, 0, -1],
            "w": [-1, 0, 1],
        }
        self.blackTiles = set()

    # 3 Axis system   https://www.redblobgames.com/grids/hexagons/
    def getTiles(self) -> int:
        for line in self.lineList:
            prev = line[0]
            currentCoord = [0, 0, 0]
            for char in line:
                if char not in "ns":
                    direction = prev + char if prev in "ns" else char
                    for i, step in enumerate(self.dirMap[direction]):
                        currentCoord[i] += step
                prev = char
            tile = tuple(currentCoord)
            if tile in self.blackTiles:
                self.blackTiles.remove(tile)
            else:
                self.blackTiles.add(tile)
        return len(self.blackTiles)

    def getAdjacentTiles(self, tile) -> List[Tuple[int]]:
        return [(tile[0] + dq, tile[1] + dr, tile[2] + dp) for dq, dr, dp in self.dirMap.values()]

    def updateTileColor(self, tile: Tuple, newBlackTiles: set) -> Set[Tuple]:
        count = 0
        if tile in self.seen:
            return newBlackTiles
        self.seen.add(tile)

        adjacentTiles = self.getAdjacentTiles(tile)
        count = sum(1 for adjTile in adjacentTiles if adjTile in self.blackTiles)

        if (tile in self.blackTiles and 0 < count <= 2) or (tile not in self.blackTiles and count == 2):
            newBlackTiles.add(tile)

        if tile not in self.blackTiles:
            return newBlackTiles
        for tile in adjacentTiles:
            newBlackTiles = self.updateTileColor(tile, newBlackTiles)
        return newBlackTiles

    def getTiles2(self) -> int:
        if not self.blackTiles:
            self.getTiles()

        for _ in range(100):
            tempBlackTiles = set()
            self.seen = set()
            for tile in self.blackTiles:
                tempBlackTiles = self.updateTileColor(tile, tempBlackTiles)
            self.blackTiles = tempBlackTiles
        return len(self.blackTiles)


if __name__ == "__main__":
    lobby = Lobby()
    print("Day 24 part 1:", lobby.getTiles())
    print("Day 24 part 2:", lobby.getTiles2())
    # Total Runtime ~1.1s
