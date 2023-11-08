from typing import Optional, Tuple


class StateAction:
    def __init__(self, val: bool, direction: int, nextState: str) -> None:
        self.val = val
        self.dir = direction
        self.next = nextState


class State:
    def __init__(self, zeroAction: StateAction, oneAction: StateAction) -> None:
        self.zero = zeroAction
        self.one = oneAction


class Turing:
    def getInput(self) -> Tuple:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        begin = ""
        steps = 0
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                line = line.strip()[:-1]
                if "Begin" in line:
                    begin = line.split(" ")[3]
                elif "Perform" in line:
                    steps = int(line.split(" ")[5])
        return begin, steps

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.begin, self.steps = self.getInput()
        # Hardcode
        if self.useTest:
            self.states = {
                "A": State(StateAction(True, 1, "B"), StateAction(False, -1, "B")),
                "B": State(StateAction(True, -1, "A"), StateAction(True, 1, "A")),
            }
        else:
            self.states = {
                "A": State(StateAction(True, 1, "B"), StateAction(False, -1, "B")),
                "B": State(StateAction(True, -1, "C"), StateAction(False, 1, "E")),
                "C": State(StateAction(True, 1, "E"), StateAction(False, -1, "D")),
                "D": State(StateAction(True, -1, "A"), StateAction(True, -1, "A")),
                "E": State(StateAction(False, 1, "A"), StateAction(False, 1, "F")),
                "F": State(StateAction(True, 1, "E"), StateAction(True, 1, "A")),
            }

    def getOnes(self) -> int:
        ones = set()
        state = self.begin
        pos = 0
        for _ in range(self.steps):
            action = self.states[state].one if pos in ones else self.states[state].zero
            ones.add(pos) if action.val else ones.discard(pos)
            pos += action.dir
            state = action.next
        return len(ones)


if __name__ == "__main__":
    turing = Turing()
    print("Day 25 part 1:", turing.getOnes())
    # Total runtime ~2s
