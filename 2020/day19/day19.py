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
            return self.manualCheck()
        return sum(message in zeroRules for message in self.messages)

    def manualCheck(self) -> None:
        total = 0
        # A bit of hard code list the problem suggests
        for message in self.messages:
            firstPart = []
            timesMatched = 0
            
            while message:
                for possibleMatch in self.convertedRule[42]:
                    if message.startswith(possibleMatch):
                        message = message[len(possibleMatch):]
                        timesMatched += 1
                        # 42 is repeated twice, so we can skip the first iteration (Hack)
                        if timesMatched > 1:
                            firstPart.append((message, timesMatched))
                        break
                else:
                    break
            
            for matchedMessage, times in firstPart:
                if self.hasMatch(matchedMessage, times, self.convertedRule[31]):
                    total += 1
                    break

        return total

    def hasMatch(self, message: str, times: int, possibleMatches: Set[str]) -> bool:
        timesMatched = 0
        while message:
            for possibleMatch in possibleMatches:
                if message.startswith(possibleMatch):
                    message = message[len(possibleMatch):]
                    timesMatched += 1
                    if len(message) == 0 and timesMatched <= times - 1:
                        return True
                    break
            else:
                break
        return False


if __name__ == "__main__":
    messages = Messages()
    print("Day 19 part 1:", messages.getZeroRuleMatches())
    print("Day 19 part 2:", messages.getZeroRuleMatches(True))
    # Total Runtime ~2.2s
