
class Folder():
    
    def getInput(self):
        file1 = open('input-test.txt', 'r')
        # file1 = open('input-test.txt', 'r')
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

    def buildFolder(self) -> int:
        for line in self.inputData:
            arguments = line.split(' ')
            #command
            if arguments[0] == '$':
                if arguments[1] == 'cd':
                    self.updateFilePath(arguments[2])
            elif arguments[0] == 'dir' and self.filePath[-1] not in  self.currentFolder:
                self.currentFolder[arguments[1]] = {}
            else:
                self.currentFolder[arguments[1]] = int(arguments[0])
        
        print(self.folder)
        pass

    def getSize(self) -> int:
        self.buildFolder()
        pass

    def updateFilePath(self, cmd: str):
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
    print(folder.getSize())