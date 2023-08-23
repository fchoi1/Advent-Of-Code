from typing import Optional, Tuple, Callable, Any, Dict, List, Set
from collections import deque
import time

def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    cache = {}

    def wrapper(self, time, valve, bitmask):
        key = (time, valve, bitmask)
        if key not in cache:
            cache[key] = func(self, time, valve, bitmask)
        return cache[key]

    return wrapper

class Valves():
    def getInput(self) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
        inputFile = 'input-test.txt' if self.useTest else 'input.txt'
        with open(inputFile, 'r') as file1:
            Lines = file1.readlines()
            valves = {}
            tunnels = {}
            for line in Lines:
                line = line.strip()
                valve = line.split()[1]
                valves[valve] = int(line.split('=')[1].split(';')[0])
                tunnels[valve] = line.split('to ', 1)[1].split(' ',1)[1].split(', ')
        return (valves, tunnels)
    
    def __init__(self, useTest: Optional[bool] = False) -> None:
        """ Main entry point of the app """
        self.useTest = useTest

        self.valves, self.tunnels = self.getInput()
        self.nonEmpty = self.getNonEmpty(self.valves)
        self.dists = self.simpify(self.valves, self.tunnels)

    def getNonEmpty(self, valves: Dict[str, int]) -> Dict[str, int]:
        nonEmpty = {}
        count = 0
        for valve, flow in valves.items():
            if flow != 0:
                nonEmpty[valve] = count
                count += 1
        return nonEmpty

    # find shortest path for each valve to each one that has not an empty flow rate
    def simpify(self, valves: Dict[str, int], tunnels:  Dict[str, List[str]]) -> Set:
        dists = {}

        for valve in valves:
            # Ignore all zero  flow rate except for AA
            if not valves[valve] and valve != "AA": 
                continue

            dists[valve] = {}
            visited = {valve}
            q = deque([(0, valve)])

            while q:
                dist, currValve = q.popleft()
                visited.add(currValve)
                for nextValve in tunnels[currValve]:
                    if nextValve in visited:
                        continue
                    # Only add onves with flow rate
                    if valves[nextValve]:                            
                        dists[valve][nextValve] = dist + 1
                    q.append((dist+1, nextValve))
        return dists
    
    # # use bitmask to represent vavle open or not, maybe a bit more efficient binary states
    @memoize
    def dfs(self, time: int, valve: str, bitmask: int) -> int:
        maxRate = 0

        if time <= 0:
            return maxRate
        
        for nextValve in self.dists[valve]:
            bit = 1 << self.nonEmpty[nextValve]
            # if valve is already open, then continue
            if bitmask & bit:
                continue
         
            timeRemain = time - self.dists[valve][nextValve] - 1
            if timeRemain <= 0:
                continue
            maxRate = max(maxRate, self.dfs(timeRemain, nextValve, bitmask | bit) + timeRemain * self.valves[nextValve] )

        return maxRate

    def getMaxRate(self, timeLength: Optional[int] = 30) -> int:
        start_time = time.time()
        maxRate = self.dfs(timeLength,'AA',0)
        end_time = time.time()
        execution_time = end_time - start_time
        print('execution  time:', execution_time) # checking difference of memmoization
        return maxRate

    def getMaxRate2(self, timeLength: Optional[int] = 26) -> int:
        start_time = time.time()
        # loop through all possible positions for 2 workers with bit partitions
        totalPositions = (1 << len(self.nonEmpty)) - 1
        maxRate = 0
        for i in range( ( totalPositions + 1) // 2): # Divide by 2 to avoid redundant calculations
            maxRate = max(maxRate, self.dfs(timeLength, 'AA', i) + self.dfs(timeLength, 'AA', totalPositions ^ i))
        end_time = time.time()
        execution_time = end_time - start_time
        print('execution  time:', execution_time) 
        return maxRate

if __name__ == "__main__":
    """ This is executed when run from the command line """
    valves = Valves(False)
    print('Day 16 part 1:', valves.getMaxRate(30))
    print('Day 16 part 2:',  valves.getMaxRate2(26))
