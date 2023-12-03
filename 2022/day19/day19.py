from typing import List, Optional
import re


#  TODO: Make this Faster using DFS instead of BFS
class Minerals:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            blueprints = []
            delimiters = [
                "Each ore robot costs ",
                " ore. Each clay robot costs ",
                " ore. Each obsidian robot costs ",
                " ore and ",
                " clay. Each geode robot costs ",
                " ore and ",
                " obsidian.",
            ]
            for line in file1:
                line = line.strip()
                prices = list(
                    map(
                        int,
                        re.split("|".join(map(re.escape, delimiters)), line.strip())[
                            1:7
                        ],
                    )
                )
                # [ore, clay, obsidian, geode]
                oreCost = [prices[0], 0, 0, 0]
                clayCost = [prices[1], 0, 0, 0]
                obsidianCost = [prices[2], prices[3], 0, 0]
                geodeCost = [prices[4], 0, prices[5], 0]
                blueprints.append((oreCost, clayCost, obsidianCost, geodeCost))
        return blueprints

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.blueprints = self.getInput()
        self.currentBlueprint = 0
        # ore: 1, clay: 2, obsidian: 3, geode: 4
        self.robots = [1, 0, 0, 0]
        self.resources = [1, 0, 0, 0]

    def updateResources(self, robots: List[int], resources: List[int]) -> List[int]:
        for i, robot in enumerate(robots):
            resources[i] += robot
        return resources.copy()

    def getMaxGeode(self, timeLength: int) -> int:
        maxGeode = 0
        blueprint = self.blueprints[self.currentBlueprint - 1]
        maxCosts = [max(col) * 2 for col in zip(*blueprint)]  # hacky solution
        maxCosts[3] = float("inf")
        q = [([1, 0, 0, 0], [0, 0, 0, 0])]
        visited = set()

        for _ in range(timeLength):
            tempQ = []

            for robots, resources in q:
                options = self.getOptions(resources)
                for i, cost in enumerate(maxCosts):
                    resources[i] = min(cost, resources[i])
                key = self.getKey(robots, resources)
                if key in visited:
                    continue
                visited.add(key)

                for i, isAllowed in options:
                    # Want only max amount of robots for max cost
                    if isAllowed and robots[i] < maxCosts[i]:
                        newRobot = robots.copy()
                        newRobot[i] += 1
                        newResources = self.buyRobot(i, resources)
                        newResources = self.updateResources(robots, newResources)

                        for i, cost in enumerate(maxCosts):
                            newResources[i] = min(cost, newResources[i])
                        key = self.getKey(newRobot, newResources)
                        if key in visited:
                            continue

                        tempQ.append((newRobot, newResources))
                        maxGeode = max(maxGeode, newResources[3])

                if not all(option[1] for option in options):
                    updatedResources = self.updateResources(robots, resources)
                    tempQ.append((robots, updatedResources))
                    maxGeode = max(maxGeode, updatedResources[3])
            q = tempQ
        return maxGeode

    def getQuality(self, time: int) -> int:
        quality = 0
        for i in range(len(self.blueprints)):
            self.currentBlueprint = i + 1
            maxG = self.getMaxGeode(time)
            quality += self.currentBlueprint * maxG
        return quality

    def getLargestGeodes(self, time: int, blueprintLength: int) -> int:
        maxProduct = 1
        for i in range(blueprintLength):
            self.currentBlueprint = i + 1
            maxG = self.getMaxGeode(time)
            maxProduct *= maxG
        return maxProduct

    def getKey(self, robot: List[int], resource: List[int]) -> str:
        return ",".join(map(str, robot + resource))

    def buyRobot(self, robotNum: int, resources: List[int]):
        blueprint = self.blueprints[self.currentBlueprint - 1]
        mineralCost = blueprint[robotNum]
        return [resource - cost for resource, cost in zip(resources, mineralCost)]

    def getOptions(self, resources: List[int]) -> List[bool]:
        blueprint = self.blueprints[self.currentBlueprint - 1]
        options = []
        for i, mineralCost in enumerate(blueprint):
            options.append(
                [
                    i,
                    all(
                        resource >= cost
                        for resource, cost in zip(resources, mineralCost)
                    ),
                ]
            )
        return options


if __name__ == "__main__":
    mineral = Minerals()
    # ~ 34 seconds runtime
    print("Day 19 part 1:", mineral.getQuality(24))
    # ~ 1 minute 24 second runtime
    print("Day 19 part 2:", mineral.getLargestGeodes(32, 3))
    # Total runtime ~ 2 minutes 20 seconds
