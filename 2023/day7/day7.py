from typing import List, Optional, Tuple
from collections import Counter


class Poker:
    def getInput(self) -> List[Tuple[str, int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            return [(h, int(b)) for x in file1 for h, b in [x.strip().split()]]

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.hands = self.getInput()

    def getType(self, hand: str, bid: int, useJ: Optional[bool] = False) -> List[int]:
        cardMap = "J23456789TQKA" if useJ else "23456789TJQKA"
        value = [cardMap.index(char) for char in hand] + [bid]
        count = Counter(hand).most_common(5)
        jokers = 0
        top = count[0][1]
        if top == 5:
            return [7] + value
        second = count[1][1]

        if useJ:
            jokers = Counter(hand).get("J", 0)
            top = count[1][1] + jokers if count[0][0] == "J" else count[0][1] + jokers
            if top == 5:
                return [7] + value
            second = count[2][1] if count[0][0] == "J" else count[1][1]

        if top == 4:
            return [6] + value
        elif top == 3 and second == 2:
            return [5] + value
        elif top == 3 and second == 1:
            return [4] + value
        elif top == 2 and second == 2:
            return [3] + value
        elif top == 2 and second == 1:
            return [2] + value
        else:
            return [1] + value

    def getWinnings(self, isPart2: Optional[bool] = False) -> int:
        score = [self.getType(hand, bid, isPart2) for hand, bid in self.hands]
        score.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4], x[5]))
        return sum(hand[-1] * (i + 1) for i, hand in enumerate(score))


if __name__ == "__main__":
    poker = Poker()
    print("Day 7 part 1:", poker.getWinnings())
    print("Day 7 part 2:", poker.getWinnings(True))
