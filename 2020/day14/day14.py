from typing import Optional, List


class Memory:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1.readlines():
                line = line.strip().split(" = ")

                if line[0] == "mask":
                    data.append(("mask", line[1]))
                    continue
                address = int(line[0].split("[")[1].split("]")[0])
                data.append(("mem", address, int(line[1])))
                # print(line)

        return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.program = self.getInput()
        print(self.program)

    def getMemorySum(self) -> int:
        pass


if __name__ == "__main__":
    memory = Memory(True)
    print("Day 14 part 1:", memory.getMemorySum())
    print("Day 14 part 2:")
