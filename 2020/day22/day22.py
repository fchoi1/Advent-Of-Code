from typing import Optional, List, Set, Tuple, Deque
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
        self.reset()

    def reset(self) -> None:
        p1, p2 = self.getInput()
        self.p1 = deque(p1)
        self.p2 = deque(p2)

    def playRecursive(self, p1Deck: Deque[int], p2Deck: Deque[int]) -> Tuple[List[int] | str]:
        seen1, seen2 = set(), set()

        while p1Deck and p2Deck:
            p1key = tuple(p1Deck)
            p2key = tuple(p2Deck)

            if p1key in seen1 or p2key in seen2:
                return (p1Deck, "p1")

            seen1.add(p1key)
            seen2.add(p2key)

            p1Val, p2Val = p1Deck.popleft(), p2Deck.popleft()

            if len(p1Deck) >= p1Val and len(p2Deck) >= p2Val:
                p1Copy = deque(list(p1Deck)[:p1Val])
                p2Copy = deque(list(p2Deck)[:p2Val])
                _, winner = self.playRecursive(p1Copy, p2Copy)
            else:
                winner = "p1" if p1Val > p2Val else "p2"

            if winner == "p1":
                p1Deck.extend([p1Val, p2Val])
            else:
                p2Deck.extend([p2Val, p1Val])

        return (p2Deck, "p2") if not p1Deck else (p1Deck, "p1")

    def playGame(self) -> List:
        while self.p1 and self.p2:
            p1Val, p2Val = self.p1.popleft(), self.p2.popleft()

            if p1Val > p2Val:
                self.p1.extend([p1Val, p2Val])
            else:
                self.p2.extend([p2Val, p1Val])

        return self.p1 if len(self.p2) == 0 else self.p2

    def getScore(self, playRecursive: Optional[bool] = False) -> int:
        self.reset()
        if playRecursive:
            winList, winner = self.playRecursive(self.p1, self.p2)
        else:
            winList = self.playGame()
        winList.reverse()
        return sum(i * card for i, card in enumerate(winList, start=1))


if __name__ == "__main__":
    crabGame = CrabGame()
    print("Day 22 part 1:", crabGame.getScore())
    print("Day 22 part 2:", crabGame.getScore(True))
