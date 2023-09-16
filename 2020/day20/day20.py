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
                    continue
                if line.split(' ')[0] == 'Tile':
                    currTile = int(line.split(' ')[1].split(':')[0])
                    continue
                tileMap.append(list(line))
        tiles[currTile] = tileMap
        return tiles

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.borders = {}
        self.tiles = self.getInput()
        self.length =  len(next(iter(self.tiles.values())))
        
        self.tileEdges = self.getEdges(self.tiles)
        # self.printTiles()

    def getEdges(self, tiles: Dict[int, List]) -> Dict[int, Tuple]:
        m = self.length - 1
        tileEdges = {}
        edgesDict = {}

        for tileId, tile in tiles.items():
            topEdge = "".join(tile[0])
            rightEdge = "".join(row[m] for row in tile)
            leftEdge = "".join(row[0] for row in tile)
            bottomEdge = "".join(tile[m])

            # not 2 edges in an image are the same
            edges = (topEdge, rightEdge, leftEdge, bottomEdge)
            tileEdges[tileId] = edges


            for edge in edges:
                if edge in edgesDict:
                    del edgesDict[edge]
                elif edge[::-1] in edgesDict:
                    del edgesDict[edge[::-1]]
                else:
                    edgesDict[edge] = tileId
        self.borders = edgesDict
        return tileEdges
    
    def getCorners(self) -> int:
        temp = set()
        total = 1
        for tileId in self.borders.values():
            if tileId in temp:
                total *= tileId
            else:
                temp.add(tileId)

        return total
    
    def printTiles(self) -> None:
        for tiles in self.tiles.values():
            print()
            for row in tiles:
                print("".join(row))

if __name__ == "__main__":
    jigsaw = Jigsaw()
    print("Day 20 part 1:",jigsaw.getCorners())
    print("Day 20 part 2:")
