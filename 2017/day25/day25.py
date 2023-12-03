from typing import Optional, Tuple


class Turing:
    def getInput(self) -> Tuple:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        begin = ""
        steps = 0
        with open(inputFile, "r") as file1:
            for line in file1:
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
                "A": [[True, 1, "B"], [False, -1, "B"]],
                "B": [[True, -1, "A"], [True, 1, "A"]],
            }
        else:
            self.states = {
                "A": [[True, 1, "B"], [False, -1, "B"]],
                "B": [[True, -1, "C"], [False, 1, "E"]],
                "C": [[True, 1, "E"], [False, -1, "D"]],
                "D": [[True, -1, "A"], [True, -1, "A"]],
                "E": [[False, 1, "A"], [False, 1, "F"]],
                "F": [[True, 1, "E"], [True, 1, "A"]],
            }

    def getOnes(self) -> int:
        ones = set()
        state = self.begin
        pos = 0
        for _ in range(self.steps):
            action = self.states[state][pos in ones]
            ones.add(pos) if action[0] else ones.discard(pos)
            pos += action[1]
            state = action[2]
        return len(ones)


if __name__ == "__main__":
    turing = Turing()
    print("Day 25 part 1:", turing.getOnes())
    # Total runtime ~2.3s
