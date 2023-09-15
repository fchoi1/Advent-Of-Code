from typing import Optional, List, Set
import itertools


class Messages:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        rulesList, messageList = {}, []
        messages = False
        with open(inputFile, "r") as file1:
            for line in file1:
                if not line.strip():
                    messages = True
                    continue
                if messages:
                    messageList.append(line.strip())
                else:
                    ruleNum, rule = line.strip().replace('"', "").split(": ")
                    ruleSplit = rule.split(" | ")
                    rulesList[int(ruleNum)] = [r.split(" ") for r in ruleSplit]
        return rulesList, messageList

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.reset()
        # print(self.rules, self.messages)

    def reset(self) -> None:
        self.rules, self.messages = self.getInput()
        self.convertedRule = {}

    def getRules(self, ruleNum: int) -> Set[str]:
        rules = self.rules[ruleNum]
        if ruleNum in self.convertedRule:
            return self.convertedRule[ruleNum]

        if len(rules) == 1 and not rules[0][0].isdigit():
            return set(rules[0])

        possibleMatchesSet = set()
        for rule in rules:
            possibleMatches = [self.getRules(int(num)) for num in rule]
            possibleMatchesSet.update("".join(match) for match in itertools.product(*possibleMatches))
        self.convertedRule[ruleNum] = possibleMatchesSet
        return possibleMatchesSet

    def getZeroRuleMatches(self, updateRules: Optional[bool] = False) -> int:
        self.reset()
        zeroRules = self.getRules(0)
        if updateRules:
            self.manualRuleChange()

        return sum(message in zeroRules for message in self.messages)

    def manualRuleChange(self) -> None:
        length = max(len(message) for message in self.messages)
        print(self.convertedRule[42])
        print(self.convertedRule[8])
        # print(self.convertedRule[31])
        ruleList = ["42", "42"]
        newConverted = self.combineRules(["42", "8"])
        currLength = max(len(element) for element in newConverted)
        # print("starrt", currLength, length)
        count = 0
        while currLength < length and count < 3:
            newConverted.update(self.combineRules(ruleList))
            ruleList.append("42")
            currLength = max(len(match) for match in newConverted)
            print(currLength)
            count += 1

        pass
        # self.convertedRule[8] = newConverted
        print("dpne!", currLength)

    def combineRules(self, rule) -> Set[str]:
        possibleMatchesSet = set()
        possibleMatches = [self.getRules(int(num)) for num in rule]
        possibleMatchesSet.update("".join(match) for match in itertools.product(*possibleMatches))
        return possibleMatchesSet


if __name__ == "__main__":
    messages = Messages(True)
    print("Day 19 part 1:", messages.getZeroRuleMatches())
    print("Day 19 part 2:", messages.getZeroRuleMatches(True))
