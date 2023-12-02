from typing import List, Optional


class Cube:
    def getInput(self) -> List[List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        games = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                sets = line.strip().split(": ")[1].split("; ")
                colors = [0, 0, 0]
                for s in sets:
                    for balls in s.split(", "):
                        ball, color = balls.split(" ")
                        i = ["red", "green", "blue"].index(color)
                        colors[i] = max(colors[i], int(ball))
                games.append(colors)
            return games

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.games = self.getInput()
        self.max = [12, 13, 14]
        self.runGames()

    def runGames(self) -> int:
        self.total = 0
        self.power = 0
        for i in range(len(self.games)):
            game = self.games[i]
            self.power += game[0] * game[1] * game[2]
            if all(game[j] <= self.max[j] for j in range(3)):
                self.total += i + 1

    def getTotal(self):
        return self.total

    def getPower(self):
        return self.power


if __name__ == "__main__":
    cube = Cube()
    print("Day 2 part 1:", cube.getTotal())
    print("Day 2 part 2:", cube.getPower())
