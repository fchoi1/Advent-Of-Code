from typing import Optional, List


class Cups:
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


if __name__ == "__main__":
    cups = Cups()
    print("Day 23 part 1:")
    print("Day 23 part 2:")
