from typing import List, Optional


class Passport:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        with open(inputFile, "r") as file1:
            data = []
            passport = {}
            for line in file1:
                line = line.strip()
                if not line:
                    data.append(passport)
                    passport = {}
                else:
                    keyValues = line.split(" ")
                    for pairs in keyValues:
                        key, value = pairs.split(":")
                        passport[key] = value
            data.append(passport)
        return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.passports = self.getInput()
        self.valid = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        self.years = [(1920, 2002), (2010, 2020), (2020, 2030)]
        self.eyeColor = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        self.hairColor = "0123456789abcdeff"
        self.pid = "0123456789"
        self.height = {"cm": (150, 193), "in": (59, 76)}

    def getValid(self) -> int:
        count = 0
        self.validPassports = []
        for passport in self.passports:
            if all(fields in passport for fields in self.valid):
                count += 1
                self.validPassports.append(passport)
        return count

    def getMoreValid(self) -> int:
        count = 0
        for passport in self.validPassports:
            if self.isValid(passport):
                count += 1
        return count

    def isValid(self, passport) -> bool:
        try:
            for i, years in enumerate(self.valid[:3]):
                if not self.years[i][0] <= int(passport[years]) <= self.years[i][1]:
                    return False
        except ValueError:
            return False

        unit = passport["hgt"][-2:]
        if unit not in ["in", "cm"]:
            return False

        try:
            if not self.height[unit][0] <= int(passport["hgt"][:-2]) <= self.height[unit][1]:
                return False
        except ValueError:
            return False

        if passport["hcl"][0] != "#" or len(passport["hcl"][1:]) != 6:
            return False

        if not all(char in self.hairColor for char in passport["hcl"][1:]):
            return False

        if passport["ecl"] not in self.eyeColor:
            return False

        try:
            if len(passport["pid"]) != 9:
                return False
            int(passport["pid"])
        except ValueError:
            return False

        return True


if __name__ == "__main__":
    passport = Passport()
    print("Day 4 part 1:", passport.getValid())
    print("Day 4 part 2:", passport.getMoreValid())
