from typing import Optional, List, Dict, Tuple


class Jigsaw:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        tiles = {}
        tileMap = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                if not line:
                    tiles[currTile] = tileMap
                    tileMap = []
                elif line.split(" ")[0] == "Tile":
                    currTile = int(line.split(" ")[1].split(":")[0])
                else:
                    tileMap.append(list(line))
        tiles[currTile] = tileMap
        return tiles

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.borders = {}
        self.corners = {}
        self.tiles = self.getInput()
        self.length = len(next(iter(self.tiles.values())))
        self.tilesMap = self.getEdges(self.tiles)
        self.monster = self.getMonsterCoords()

    def getMonsterCoords(self) -> List[Tuple[int]]:
        pattern = [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   ",
        ]
        coordinates = []
        for y, row in enumerate(pattern):
            for x, char in enumerate(row):
                if char == "#":
                    coordinates.append((x, y))

        return [(x, y) for x, y in coordinates]

    def countMonsters(self, picture: List[List[str]]) -> int:
        map_height = len(picture)
        map_width = len(picture[0])
        monster_count = 0

        for y in range(map_height):
            for x in range(map_width):
                is_monster = True
                for dx, dy in self.monster:
                    new_x, new_y = x + dx, y + dy

                    if (
                        new_x < 0
                        or new_x >= map_width
                        or new_y < 0
                        or new_y >= map_height
                        or picture[new_y][new_x] != "#"
                    ):
                        is_monster = False
                        break

                if is_monster:
                    monster_count += 1

        return monster_count

    def getEdges(self, tiles: Dict[int, List]) -> Dict[int, Tuple]:
        m = self.length - 1
        tileEdges = {}
        edgesDict = {}

        for tileId, tile in tiles.items():
            topEdge = "".join(tile[0])
            rightEdge = "".join(row[m] for row in tile)
            leftEdge = "".join(row[0] for row in tile)
            bottomEdge = "".join(tile[m])

            edges = (topEdge, rightEdge, bottomEdge, leftEdge)

            for i, edge in enumerate(edges):
                if edge in tileEdges:
                    tileEdges[edge].append((tileId, i))
                else:
                    tileEdges[edge] = [(tileId, i)]
                if edge in edgesDict:
                    del edgesDict[edge]
                elif edge[::-1] in edgesDict:
                    del edgesDict[edge[::-1]]
                else:
                    edgesDict[edge] = (tileId, i)
        self.borders = edgesDict
        return tileEdges

    def getCorners(self) -> int:
        temp = set()
        total = 1
        for tileId, _ in self.borders.values():
            if tileId in temp:
                total *= tileId
                self.corners[tileId] = [tile[1] for tile in self.borders.values() if tileId == tile[0]]
            else:
                temp.add(tileId)
        return total

    def flip(self, tile: List[List[str]], axis: str) -> List[List[str]]:
        if axis == "y":
            return [row[::-1] for row in tile]
        elif axis == "x":
            return tile[::-1]
        return tile

    def rotate(self, tile: List[List[str]], direction: str) -> List[List[str]]:
        if direction == "about":
            return self.flip(self.flip(tile, "x"), "y")
        elif direction == "right":
            return [list(row) for row in zip(*reversed(tile))]
        elif direction == "left":
            return [list(row) for row in reversed(list(zip(*tile)))]
        else:
            return tile

    def getMonsters(self) -> int:
        monsters = 0
        picture = self.removeBorders(self.buildPicture())
        # self.printPicture(picture) # for debug
        for _ in range(2):
            for _ in range(3):
                picture = self.rotate(picture, "left")
                monsters = max(monsters, self.countMonsters(picture))
            picture = self.flip(picture, "x")

        return sum(row.count("#") for row in picture) - monsters * len(self.monster)

    def printPicture(self, picture: List[List[str]]) -> None:
        print(picture)
        for row in picture:
            print("".join(row))

    def removeBorders(self, picture: List) -> List[List[str]]:
        updatedPicture = []
        for pictureRow in picture:
            for i in range(1, len(pictureRow[0]) - 1):
                strRow = "".join(["".join(tile[i][1 : self.length - 1]) for tile in pictureRow])
                updatedPicture.append(list(strRow))
        return updatedPicture

    def buildPicture(self) -> List[List[str]]:
        picture = []
        row = []
        m = self.length - 1
        for tileId, corner in self.corners.items():
            if corner == [0, 3]:
                currTile = self.tiles[tileId]
                currTileId = rowId = tileId
                row.append(currTile)
                break
        else:
            if corner == [0, 1]:
                currTile = self.flip(self.tiles[tileId], "y")
                currTileId = rowId = tileId
                row.append(currTile)
        isFirst = True

        while True:
            if isFirst:
                isFirst = False
            else:
                row = []
                currTileId = rowId
                bottomEdge = "".join(picture[-1][0][m])

                if bottomEdge in self.tilesMap and not all(
                    currTileId == tileId for tileId, _ in self.tilesMap[bottomEdge]
                ):
                    for tileId, pos in self.tilesMap[bottomEdge]:
                        if currTileId != tileId:
                            currTileId = rowId = tileId
                            break

                    currTile = self.tiles[currTileId]
                    if pos == 1:  # right
                        currTile = self.rotate(currTile, "left")
                    elif pos == 2:  # bottom
                        currTile = self.flip(currTile, "x")
                    elif pos == 3:  # left
                        currTile = self.flip(self.rotate(currTile, "right"), "y")
                elif bottomEdge[::-1] in self.tilesMap and not all(
                    currTileId == tileId for tileId, _ in self.tilesMap[bottomEdge[::-1]]
                ):
                    for tileId, pos in self.tilesMap[bottomEdge[::-1]]:
                        if currTileId != tileId:
                            currTileId = rowId = tileId
                            break

                    currTile = self.tiles[currTileId]
                    if pos == 0:  # top
                        currTile = self.flip(currTile, "y")
                    if pos == 1:  # right
                        currTile = self.flip(self.rotate(currTile, "left"), "y")
                    elif pos == 2:  # bottom
                        currTile = self.rotate(currTile, "about")
                    elif pos == 3:  # left
                        currTile = self.rotate(currTile, "right")
                else:
                    break
                row.append(currTile)

            while True:
                rightEdge = "".join(row[m] for row in currTile)
                if rightEdge in self.tilesMap and not all(
                    currTileId == tileId for tileId, _ in self.tilesMap[rightEdge]
                ):
                    for tileId, pos in self.tilesMap[rightEdge]:
                        if currTileId != tileId:
                            currTileId = tileId
                            break
                    currTile = self.tiles[currTileId]
                    if pos == 0:  # top
                        currTile = self.flip(self.rotate(currTile, "left"), "x")
                    elif pos == 1:  # right
                        currTile = self.flip(currTile, "y")
                    elif pos == 2:  # bottom
                        currTile = self.rotate(currTile, "right")
                    row.append(currTile)
                elif rightEdge[::-1] in self.tilesMap and not all(
                    currTileId == tileId for tileId, _ in self.tilesMap[rightEdge[::-1]]
                ):
                    for tileId, pos in self.tilesMap[rightEdge[::-1]]:
                        if currTileId != tileId:
                            currTileId = tileId
                            break
                    else:
                        break

                    currTile = self.tiles[currTileId]
                    if pos == 0:  # top
                        currTile = self.rotate(currTile, "left")
                    elif pos == 1:  # right
                        currTile = self.rotate(currTile, "about")
                    elif pos == 2:  # bottom
                        currTile = self.flip(self.rotate(currTile, "right"), "x")
                    elif pos == 3:  # left
                        currTile = self.flip(currTile, "x")
                    row.append(currTile)
                else:
                    break
            picture.append(row)
        return picture


if __name__ == "__main__":
    jigsaw = Jigsaw()
    print("Day 20 part 1:", jigsaw.getCorners())
    print("Day 20 part 2:", jigsaw.getMonsters())
