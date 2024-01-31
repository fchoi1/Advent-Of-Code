class intCodeComputer:
    def __init__(
        self, programCode, id=0, relBase=0, indx=0, emptySpace=1000, inptArr=[]
    ):
        self.relativeBase = 0
        self.memory = []
        self.memory = programCode.copy()
        for i in range(emptySpace):
            self.memory.append(0)
        self.index = indx
        self.inputArray = inptArr.copy()
        self.outputArray = []
        self.id = id
        self.finished = False

    def compute(self):  # computes until there's an input requiered
        while True:
            if self.index == 308:
                print(self.memory[311])
            # formatting OPCODE

            TempLen = len(str(self.memory[self.index]))
            StringToAdd = ""
            for i in range(5 - TempLen):
                StringToAdd += "0"
            self.memory[self.index] = StringToAdd + str(self.memory[self.index])
            # print(self.memory[self.index])

            # reading parameters according to the given parameter modes ----------------------
            parameters = []
            parameterMode = str(self.memory[self.index][:3])
            # print(self.memory[self.index], parameterMode)
            # print(parameterMode)
            OpCode = str(self.memory[self.index])[-2:]
            self.memory[self.index] = int(self.memory[self.index])
            if parameterMode[2] == "0":
                parameters.append(int(self.memory[self.index + 1]))
            elif parameterMode[2] == "1":
                parameters.append(self.index + 1)
            else:  # paramMode 2
                parameters.append(int(self.memory[self.index + 1]) + self.relativeBase)

            if parameterMode[1] == "0":
                parameters.append(int(self.memory[self.index + 2]))
            elif parameterMode[1] == "1":
                parameters.append(self.index + 2)
            else:  # paramMode 2
                parameters.append(self.memory[self.index + 2] + self.relativeBase)

            if parameterMode[0] == "0":
                parameters.append(int(self.memory[self.index + 3]))
            elif parameterMode[0] == "1":
                parameters.append(self.index + 3)
            else:  # paramMode 2
                parameters.append(int(self.memory[self.index + 3]) + self.relativeBase)
            # param read end -----------------------------------------
            # strr=""
            # for i in range(4):
            #    strr += str(self.memory[self.index + i ] ) +"/"
            # print(self.index,strr,OpCode)
            # strr2 =""
            # for i in range(3):
            # strr2 += str(self.memory[parameters[i]] ) +"/"
            # print(strr2)
            # print("opcode:" + str(OpCode) + "  parameters: " + str(self.memory[parameters[0]]) +"/"+ str(
            # self.memory[parameters[1]]) +"/"+ str(self.memory[parameters[2]]))

            # reacting according to the OP CODE-----------------------------------------
            if OpCode == "01":
                self.memory[parameters[2]] = int(self.memory[parameters[0]]) + int(
                    self.memory[parameters[1]]
                )
                self.index += 4
            elif OpCode == "02":
                self.memory[parameters[2]] = int(self.memory[parameters[0]]) * int(
                    self.memory[parameters[1]]
                )
                self.index += 4
            elif OpCode == "03":
                if len(self.inputArray) != 0:
                    self.memory[parameters[0]] = self.inputArray[0]
                    self.index += 2
                    self.inputArray.pop(0)
                else:
                    print("waiting input", self.index)
                    break
            elif OpCode == "04":
                # print(
                #     "output from int comp "
                #     + str(self.id)
                #     + "  :"
                #     + str(self.memory[parameters[0]])
                # )
                self.outputArray.append(self.memory[parameters[0]])
                self.index += 2
            elif OpCode == "05":
                if self.memory[parameters[0]] != 0:
                    self.index = int(self.memory[parameters[1]])
                else:
                    self.index += 3
            elif OpCode == "06":
                # print("went here")
                if self.memory[parameters[0]] == 0:
                    self.index = int(self.memory[parameters[1]])
                else:
                    self.index += 3
            elif OpCode == "07":
                if int(self.memory[parameters[0]]) < int(self.memory[parameters[1]]):
                    self.memory[parameters[2]] = 1
                else:
                    self.memory[parameters[2]] = 0
                self.index += 4
            elif OpCode == "08":
                if self.memory[parameters[0]] == self.memory[parameters[1]]:
                    self.memory[parameters[2]] = 1
                else:
                    self.memory[parameters[2]] = 0
                self.index += 4
            elif OpCode == "09":
                self.relativeBase += self.memory[parameters[0]]
                self.index += 2
                # print("relative base has been changed")
            elif OpCode == "99":
                print(str(self.id) + ". computer has finished")
                self.finished = True
                break

            # print(self.relativeBase)

    def addInput(self, input):
        self.inputArray.append(input)


data = open("input.txt").read().split(",")
for i in range(len(data)):
    data[i] = int(data[i])

hull = []
hullSize = 500
for i in range(hullSize):
    hull.append([])
    for j in range(hullSize):
        hull[i].append([])
        hull[i][j] = [0, 0]  # [colour, 0 if never painted / 1 if it has]

direction = 0  # 0 up / 1 right / 2 down / 3 left
posX = posY = int(hullSize / 2)


comp0 = intCodeComputer(programCode=data)

comp0.addInput(hull[posX][posY][0])
index = 0
while comp0.finished is not True and index < 15:
    index += 1
    comp0.compute()
    print(
        posX - 250,
        posY - 250,
        "input",
        hull[posX][posY][0],
        "out",
        comp0.outputArray[-2:],
    )
    outputFromComp = comp0.outputArray[-2:]

    hull[posX][posY][0] = outputFromComp[0]
    hull[posX][posY][1] = 1

    if direction == 0:
        if outputFromComp[1] == 0:
            direction = 3
            posX -= 1
        elif outputFromComp[1] == 1:
            direction = 1
            posX += 1
        else:
            print("what the hell is going on")
    elif direction == 1:
        if outputFromComp[1] == 0:
            direction = 0
            posY -= 1
        elif outputFromComp[1] == 1:
            direction = 2
            posY += 1
        else:
            print("what the hell is going on")
    elif direction == 2:
        if outputFromComp[1] == 0:
            direction = 1
            posX += 1
        elif outputFromComp[1] == 1:
            direction = 3
            posX -= 1
        else:
            print("what the hell is going on")
    elif direction == 3:
        if outputFromComp[1] == 0:
            direction = 2
            posY += 1
        elif outputFromComp[1] == 1:
            direction = 0
            posY -= 1
        else:
            print("what the hell is going on")
    else:
        print("something has gone terribly wrong my dude")
    comp0.addInput(hull[posX][posY][0])

totalCount = 0
for i in range(hullSize):
    for j in range(hullSize):
        if hull[i][j][1] == 1:
            totalCount += 1
print(totalCount)
