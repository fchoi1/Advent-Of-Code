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
                elif line.split(' ')[0] == 'Tile':
                    currTile = int(line.split(' ')[1].split(':')[0])
                else:
                    tileMap.append(list(line))
        tiles[currTile] = tileMap
        return tiles

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.borders = {}
        self.corners = {}
        self.tiles = self.getInput()
        self.length =  len(next(iter(self.tiles.values())))
        self.picture = []
        self.tilesMap = self.getEdges(self.tiles)
        # self.printTiles()

    def getEdges(self, tiles: Dict[int, List]) -> Dict[int, Tuple]:
        m = self.length - 1
        tileEdges, edgesDict = {}, {}

        for tileId, tile in tiles.items():
            topEdge = "".join(tile[0])
            rightEdge = "".join(row[m] for row in tile)
            leftEdge = "".join(row[0] for row in tile)
            bottomEdge = "".join(tile[m])

            edges = (topEdge, rightEdge, bottomEdge, leftEdge)
            

            for i, edge in enumerate(edges):
                tileEdges[edge] = (tileId, i)
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
        if axis == 'y':
            return [row[::-1] for row in tile]
        elif axis == 'x':
            return tile[::-1]
        return tile

    def rotate(self, tile: List[List[str]], direction: str) -> List[List[str]]:
        if direction == "about":
            return self.flip(self.flip(tile, 'x'), 'y')
        elif direction == 'right':
            return [list(row) for row in zip(*reversed(tile))]
        elif direction == 'left':
            return [list(row) for row in reversed(list(zip(*tile)))]
        else:
            return tile

    def getMonsters(self) -> int:
        self.buildPicture()
        pass

    def buildPicture(self) -> None:
        # start
        print(self.corners)
        print(self.borders)
        for tileId, corner in self.corners.items():
            if corner == [0, 3]:
                currTile = self.tiles[tileId]
                self.picture.append(currTile)
                break
        else:
            if corner == [0,1]:
                currTile = self.flip(self.tiles[tileId], 'y')
                self.picture.append(currTile)
            pass

        #first row is coner
        # last row
        # left to right and stop at edge, then go down one level
        isEnd = False
        isCornerRow = True
        m = self.length - 1
        while self.tiles:
            while not isEnd:
                rightEdge = "".join(row[m] for row in currTile)
                if rightEdge in self.tilesMap:
                    tileId, pos = self.tilesMap[rightEdge]
                    currTile = self.tiles[tileId]
                    # right
                    if pos == 1:
                        currTile = self.flip(currTile, 'y')
                    # top
                    elif pos == 0:
                        currTile = self.flip(self.rotate(currTile, 'left'), 'x')
                    # bottom
                    elif pos == 2: 
                        currTile = self.rotate(currTile, 'right')

                elif reversed(rightEdge) in self.tilesMap:
                    tileId, pos = self.tilesMap[reversed(rightEdge)]
                    currTile = self.tiles[tileId]
                    # if left
                    if pos == 3:
                        currTile = self.flip(currTile, 'x')
                    # right
                    if pos == 1:
                        currTile = self.rotate(currTile, 'about')
                    # bottom
                    elif pos == 0:
                        currTile = self.flip(self.rotate(currTile, 'right'), 'x')
                    elif pos == 2: 
                        currTile = self.rotate(currTile, 'left')
                else:
                    print('No match!, should be end')
                    isEnd = True
                self.picture.append(currTile)

                if isCornerRow:
                    pass
                else:
                    pass
        


        # self.printTile(self.tiles[3079])
        # self.printTile(self.flip(self.tiles[3079], 'x'))
        # self.printTile(self.flip(self.tiles[3079], 'y'))

        pass

    def printTile(self, tile) -> None:
        print()
        for row in tile:
            print("".join(row))
        pass

    def printTiles(self) -> None:
        for tiles in self.tiles.values():
            print()
            for row in tiles:
                print("".join(row))

if __name__ == "__main__":
    jigsaw = Jigsaw(True)
    print("Day 20 part 1:", jigsaw.getCorners())
    print("Day 20 part 2:", jigsaw.getMonsters())
