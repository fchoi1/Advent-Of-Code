from typing import Optional, List


def toBinaryList(binary: int | str, length: Optional[int] = 36):
    if isinstance(binary, int):
        binary_string = bin(binary)[2:]
    elif isinstance(binary, str) and binary.startswith("0b"):
        binary_string = binary[2:]
    else:
        raise ValueError("Unsupported input format")
    return binary_string.zfill(length)


class Memory:
    def getInput(self) -> List:
        inputFile = "input-test.txt" if self.useTest else "input.txt"
        data = []
        with open(inputFile, "r") as file1:
            for line in file1:
                line = line.strip().split(" = ")
                if line[0] == "mask":
                    data.append(("mask", line[1]))
                    continue
                address = int(line[0].split("[")[1].split("]")[0])
                data.append(("mem", address, int(line[1])))
        return data

    def __init__(self, useTest: Optional[bool] = False) -> None:
        self.useTest = useTest
        self.program = self.getInput()
        self.bitmask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.memory = {}

    def mask(self, binary: bin) -> int:
        binaryStr = toBinaryList(binary)
        newBinary = ""
        for i, val in enumerate(self.bitmask):
            if val == "X":
                newBinary += binaryStr[i]
                continue
            newBinary += val
        return int(newBinary, 2)

    def addressMask(self, binary: bin) -> int:
        binaryStr = toBinaryList(binary)
        newBinary = ""
        for i, val in enumerate(self.bitmask):
            if val == "X":
                newBinary += "X"
                continue
            newBinary += "1" if int(val) or int(binaryStr[i]) else "0"

        return self.getAddressList(newBinary, [])

    def getAddressList(self, binaryStr: str, addressList: List[int]) -> List[int]:
        if "X" in binaryStr:
            newBinary = binaryStr.replace("X", "0", 1)
            newBinary2 = binaryStr.replace("X", "1", 1)
            addressList = self.getAddressList(newBinary, addressList)
            addressList = self.getAddressList(newBinary2, addressList)
        else:
            addressList.append(int(binaryStr, 2))

        return addressList

    def runProgram(self, decodeAddress: Optional[bool] = False) -> None:
        for command, *args in self.program:
            if command == "mask":
                self.bitmask = args[0]
                continue

            if not decodeAddress:
                value = self.mask(args[1])
                addressList = [args[0]]
            else:
                value = args[1]
                addressList = self.addressMask(args[0])
            for address in addressList:
                self.memory[address] = value

    def getMemorySum(self, decodeAddress: Optional[bool] = False) -> int:
        self.memory = {}
        self.runProgram(decodeAddress)
        return sum(value for value in self.memory.values())


if __name__ == "__main__":
    memory = Memory()
    print("Day 14 part 1:", memory.getMemorySum())
    print("Day 14 part 2:", memory.getMemorySum(True))
