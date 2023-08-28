from typing import List, Optional
import re


class MonkeyMap:
    def getInput(self) -> List[int]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        delimiters = [""]
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                line = line.replace('\n', "")
                line = re.split("|".join(map(re.escape, delimiters)), line)[1:-1]
                data.append(line)
            return [data[:-2], ''.join(data[len(data)-1])]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        """Main entry point of the app"""
        self.useTest = useTest
        self.map, self.directions = self.getInput()
        self.directions  = self.parseDirections(self.directions)
        self.start = self.getStart()

        self.dirCycle = ['R', 'D', 'L', 'U']
        self.dirMap = {
            'R': [ 1, 0],
            'D': [ 0, 1],
            'L': [-1, 0],
            'U': [ 0,-1]
        }
        self.dirIndex = 0

    def getStart(self):
        for i, val in enumerate(self.map[0]):
            if val == '.':
                return [0, i]
        return None            
    
    def parseDirections(self, dirString: str):
        directions = []
        numStr = ''
        for val in dirString:
            if val.isupper():
                directions.append(int(numStr))
                directions.append(val)
                numStr = ''
                continue
            numStr += val
        directions.append(int(numStr))
        return directions

    def getPassword(self):
        currDir = self.start
        for direction in self.directions:
            
            if isinstance(direction, int):
                currDir = self.dirCycle[self.dirIndex % 4]
                dx, dy = self.dirMap[currDir]

                for i in direction:
                    currDir[0] += dx
                    currDir[1] += dy


                continue
            
            self.dirIndex += 1 if direction == 'R' else -1


        pass
        # for direction in self.directions:

    def isWall(self, coords: List[int]) -> bool:
        x, y = coords
        length = self.map[y]

        
        
        return self.map[y][x] == "#"

    def getWrapCoords(self, coords: List[int], currDir: str) -> List[int]:
        x,y = coords

        if currDir == 'R':
            if x > len(self.map[y]) or self.map[y][x] == ' ':
                x = len(self.map[y]) 
                while x > 0 and self.map[y][x] != ' ':
                    x -= 1
                x += 1


        elif currDir == 'L':
            if x < 0 or self.map[y][x] == ' ':
                if x < 0:
                    x = 0
                while x < len(self.map[y]) and self.map[y][x] != ' ':
                    x += 1
                x -= 1

        elif currDir == 'U':
            if y < 0 or self.map[y][x] == ' ':
                y = 0
                while y < len(self.map) and self.map[y][x] != ' ':
                    y += 1
                y -= 1

        elif currDir == 'D':
            # if y is passed map
            if y > len(self.map) or self.map[y][x] == ' ':
                y = len(self.map)
                while y > 0 and self.map[y][x] != ' ':
                    y -= 1
                y += 1
            
        return coords

if __name__ == "__main__":
    """This is executed when run from the command line"""
    monkeyMap = MonkeyMap(True)
    print("Day 22 part 1:" )
    print("Day 22 part 2:")
