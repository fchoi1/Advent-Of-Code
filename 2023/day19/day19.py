from typing import List, Optional, Tuple, Dict
import copy


class Aplenty:
    def getInput(self) -> Tuple[Dict[str, List[str]], List[int]]:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        workflows = {}
        inputs = []
        arr = workflows
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip()
                if not line:
                    arr = inputs
                    continue
                if arr == workflows:
                    name = line.split("{")[0]
                    cond = [x.split(":") for x in line.split("{")[1][:-1].split(",")]
                    workflows[name] = cond
                elif arr == inputs:
                    arr.append([int(x.split("=")[1]) for x in line[1:-1].split(",")])
            return workflows, inputs

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.workflows, self.inputs = self.getInput()

    def runWorkflow(self, xmas: List[int]) -> str:
        wf = "in"
        while wf in self.workflows or wf not in "RA":
            for condition in self.workflows[wf]:
                if len(condition) == 1:
                    wf = condition[0]
                    break
                exp, wf = condition
                val = xmas["xmas".index(exp[0])]
                if eval(exp, {exp[0]: val}):
                    break
        return wf

    def getTotal(self) -> int:
        total = 0
        for xmas in self.inputs:
            res = self.runWorkflow(xmas)
            if res == "A":
                total += sum(xmas)
        return total

    def dfs(self, wf: str, state: List[int]) -> None:
        if wf == "R":
            return
        if wf == "A":
            product = 1
            for vals in state:
                product *= len(vals)
            self.combo += product
            return
        conditions = self.workflows[wf]
        for c in conditions:
            if len(c) == 1:
                self.dfs(c[0], state)
                continue
            exp, wf = c
            i = "xmas".index(exp[0])
            temp = copy.deepcopy(state)
            gt = ">" in exp
            cutoff = exp.split(">")[1] if gt else exp.split("<")[1]
            split = state[i].index(int(cutoff))
            if gt:
                temp[i] = state[i][split:]
                state[i] = state[i][:split]
            else:
                temp[i] = state[i][: split - 1]
                state[i] = state[i][split - 1 :]
            self.dfs(wf, temp)

    def getCombinations(self) -> int:
        self.combo = 0
        state = [list(range(0, 4000)) for _ in range(4)]
        self.dfs("in", state)
        return self.combo


if __name__ == "__main__":
    aplenty = Aplenty(True)
    print("Day 19 part 1:", aplenty.getTotal())
    print("Day 19 part 2:", aplenty.getCombinations())
    # Total Runtime ~1.6s
