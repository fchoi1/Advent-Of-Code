from typing import Optional, List
from collections import deque


class CrabGame:
    def getInput(self) -> List[List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        deck = []
        cards = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                if not line or line == "Player 1:":
                    continue
                if line == "Player 2:":
                    deck.append(cards)
                    cards = []
                    continue
                cards.append(int(line))
        deck.append(cards)
        return deck

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        p1, p2 = self.getInput()
        self.p1 = deque(p1)
        self.p2 = deque(p2)

    def playRounds(self) -> List:
        while self.p1 and self.p2:
            p1Val, p2Val = self.p1.popleft(), self.p2.popleft()

            if p1Val > p2Val:
                self.p1.extend([p1Val, p2Val])
            else:
                self.p2.extend([p2Val, p1Val])

        return self.p1 if len(self.p2) == 0 else self.p2

    def getScore(self) -> int:
        winList = self.playRounds()
        winList.reverse()

        return sum(i * card for i, card in enumerate(winList, start=1))


if __name__ == "__main__":
    crabGame = CrabGame()
    print("Day 22 part 1:", crabGame.getScore())
    print("Day 22 part 2:")
