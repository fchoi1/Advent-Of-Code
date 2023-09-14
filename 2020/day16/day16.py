from typing import Optional, List
from functools import reduce
import re


class Ticket:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            delimiters = "|".join(map(re.escape, [": ", " or ", "-"]))
            count = 0
            rules, otherTickets, departureIndex = [[] for _ in range(3)]
            for row, line in enumerate(file1):
                line = line.strip()
                if not line:
                    continue
                if line == "your ticket:" or line == "nearby tickets:":
                    count += 1
                    continue
                if count == 0:
                    splited = re.split(delimiters, line)
                    if "departure" in splited[0]:
                        departureIndex.append(row)
                    rules.append([(int(splited[1]), int(splited[2])), (int(splited[3]), int(splited[4]))])
                if count == 1:
                    currTicket = [int(x) for x in line.split(",")]
                if count == 2:
                    otherTickets.append([int(x) for x in line.split(",")])

        return (departureIndex, rules, currTicket, otherTickets)

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.departureIndex, self.rules, self.currTicket, self.otherTickets = self.getInput()
        self.scanError = 0
        self.length = len(self.currTicket)

        self.positions = [None] * self.length
        self.validTickets = [[col] for col in self.getPossibleTicket(self.currTicket)]
        self.checkTickets()

    def getPossibleTicket(self, ticket: List[int]) -> List[List[int]]:
        possibleTicket = []
        for field in ticket:
            validRules = []
            for i, ranges in enumerate(self.rules):
                if any(low <= field <= high for low, high in ranges):
                    validRules.append(i)
            possibleTicket.append(validRules)
        return possibleTicket

    def checkTickets(self) -> None:
        for ticket in self.otherTickets:
            possibleTicket = self.getPossibleTicket(ticket)
            for i, rule in enumerate(possibleTicket):
                if not rule:
                    self.scanError += ticket[i]
                    break
            else:
                for i, field in enumerate(possibleTicket):
                    self.validTickets[i].append(field)

    def getScanError(self) -> int:
        return self.scanError

    def getTicketPosition(self) -> int:
        intersections = []
        # Get Intsections
        for i, possibleFields in enumerate(self.validTickets):
            intersection = reduce(lambda x, y: set(x) & set(y), possibleFields)
            if len(intersection) == 1:
                self.positions[i] = next(iter(intersection))
                intersections.append(set())
            else:
                intersections.append(intersection)

        # Filter out the positions
        for _ in range(self.length):
            for i, intersection in enumerate(intersections):
                to_remove = set()
                for n in intersection:
                    if n in self.positions:
                        to_remove.add(n)
                intersection.difference_update(to_remove)

                if len(intersection) == 1:
                    self.positions[i] = next(iter(intersection))
                    intersection.remove(self.positions[i])

    def getDeparturePosition(self) -> int:
        self.getTicketPosition()
        if None in self.positions:
            return -1
        product = 1
        for i in self.departureIndex:
            product *= self.currTicket[self.positions.index(i)]
        return product


if __name__ == "__main__":
    ticket = Ticket()
    print("Day 16 part 1:", ticket.getScanError())
    print("Day 16 part 2:", ticket.getDeparturePosition())
