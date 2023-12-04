from typing import List, Optional
import re


class Scratchcards:
    def getInput(self) -> List[List[List[int]]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        cards = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                _, nums = line.split(": ")
                win, card = map(
                    lambda x: list(map(int, x.split())),
                    re.split(r" {1,2}\| {1,2}", nums),
                )
                cards.append([win, card])

        return cards

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.cards = self.getInput()
        self.winCards = [0] * len(self.cards)
        self.total = 0
        self.checkCards()

    def checkCards(self) -> None:
        for i, [win, card] in enumerate(self.cards):
            count = sum(c in win for c in card)
            self.winCards[i] += 1
            if count > 0:
                self.total += 2 ** (count - 1)
                currWin = self.winCards[i]
                for j in range(1, count + 1):
                    self.winCards[i + j] += currWin

    def getTotal(self) -> int:
        return self.total

    def getCards(self) -> int:
        return sum(self.winCards)


if __name__ == "__main__":
    scratchcards = Scratchcards()
    print("Day 4 part 1:", scratchcards.getTotal())
    print("Day 4 part 2:", scratchcards.getCards())
