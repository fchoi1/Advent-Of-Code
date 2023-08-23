from typing import List, Dict, Any

class Folder():
    
    def getInput(self) -> List[str]:
        file1 = open('input.txt', 'r')
        #file1 = open('input-test.txt', 'r')
        Lines = file1.readlines()
        data = []
        # Get input data
        for line in Lines:
            data.append(line.strip())
        return data

    def __init__(self) -> None:
        """ Main entry point of the app """
        self.inputData = self.getInput()
        self.folder = {}
        self.filePath = []
        self.currentFolder = self.folder
        self.sizeSum = 0

        self.totalSize = 70000000
        self.buildFolder()
        self.currentFolderSize = self.getFolderSize(self.folder)
        self.deleteSize = 30000000 - (self.totalSize - self.currentFolderSize)
        self.folderToDelete = None
        self.folderToDeleteSize = float('inf')

    def buildFolder(self) -> int:
        for line in self.inputData:
            arguments = line.split(' ')
            #command
            if arguments[0] == '$':
                if arguments[1] == 'cd':
                    self.updateFilePath(arguments[2])
            elif arguments[0] == 'dir' and self.filePath[-1] not in self.currentFolder:
                self.currentFolder[arguments[1]] = {}
            elif arguments[0].isdigit():
                self.currentFolder[arguments[1]] = int(arguments[0])
        #print(self.folder)
        pass

    def getFolderSize(self, folder: Dict[str, Any]) -> int:
        size = 0
        for item in folder:
            if isinstance(folder[item], int):
                size += folder[item]
            else:
                size += self.getFolderSize(folder[item])
        return size

    def calculateSizeSum(self, folder:Dict[str, Any], maxSize: int=100000) -> int:
        for item in folder:
            if not isinstance(folder[item], int):
                self.calculateSizeSum(folder[item])
                folderSize = self.getFolderSize(folder[item])

                if folderSize < maxSize:
                    self.sizeSum += folderSize

                if folderSize > self.deleteSize and folderSize < self.folderToDeleteSize:
                    self.folderToDelete = item
                    self.folderToDeleteSize = folderSize
        pass

    def getFoldertoDelete(self) -> int:
        return int(self.folderToDeleteSize)
        
    def getSizeSum(self) -> int:
        self.calculateSizeSum(self.folder)
        return self.sizeSum
    
    def updateFilePath(self, cmd: str) -> None:
        if cmd == '..':
            self.filePath.pop()
            self.currentFolder = self.folder
            for dir in self.filePath:
                self.currentFolder = self.currentFolder[dir]
        else:
            if cmd not in self.currentFolder:
                self.currentFolder[cmd] = {}
            self.filePath.append(cmd)
            self.currentFolder = self.currentFolder[cmd]            

if __name__ == "__main__":
    """ This is executed when run from the command line """
    folder = Folder()
    print('Day 7 part 1:', folder.getSizeSum())
    print('Day 7 part 2:', folder.getFoldertoDelete())
