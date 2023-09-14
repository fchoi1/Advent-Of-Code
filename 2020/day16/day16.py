from typing import Optional, List
import re


class Ticket:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        count = 0
        with open(inputFile, "r") as file1:
            delimiters = "|".join(map(re.escape, [": ", " or ", "-"]))
            rules = []
            otherTickets = []
            for line in file1.readlines():
                line = line.strip()
                if not line:
                    continue
                if line == "your ticket:":
                    count += 1
                    continue
                elif line == "nearby tickets:":
                    count += 1
                    continue
                if count == 0:
                    splited = re.split(delimiters, line)

                    rules.append([(int(splited[1]), int(splited[2])), (int(splited[3]), int(splited[4]))])
                if count == 1:
                    currTicket = [int(x) for x in line.split(",")]
                if count == 2:
                    otherTickets.append([int(x) for x in line.split(",")])

        return (rules, currTicket, otherTickets)

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.rules, self.currTicket, self.otherTickets = self.getInput()
        print(self.rules, self.currTicket, self.otherTickets)

    def getScanError(self) -> int:
        pass


if __name__ == "__main__":
    ticket = Ticket(True)
    print("Day 16 part 1:", ticket.getScanError())
    print("Day 16 part 2:")
