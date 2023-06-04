class FileHandler:
    def __init__(self, fileName):
        self.fileName = fileName

    def checkFile(self):
        try:
            with open(self.fileName, 'r') as file:
                link = file.read()
                if link == None:
                    exit(0)
                return str(link)
        except IOError:
            print('no file: ' + self.fileName)
            exit(0)

    def overrideFile(self, link):
        try:
            with open(self.fileName, 'w') as file:
                file.write(link)
        except IOError:
            print('cannot override file')

    def appendToFile(self, link):
        link = link.replace ( "\n", "" ) + "\n"
        try:
            with open(self.fileName, 'a') as file:
                file.write(link)
        except IOError:
            print('cannot override file')

    def lineCount(self):
        try:
            with open(self.fileName, 'r') as file:
                return sum(1 for line in file)
        except IOError:
            print('cannot access file: ' + self.fileName)
            exit(0)

    def getLineByIndex(self, lineIndex):
        try:
            with open(self.fileName, 'r') as file:
                for i, line in enumerate(file):
                    if i == lineIndex:
                        return line.replace ( "\n", "" )

                    if i > lineIndex:
                        print('out of bounds error while reading lines')
                        exit(0)

                return -1
        except IOError:
            print('cannot access file: ' + self.fileName)
            exit(0)

    def excludeLine(self, link):
        link = link.replace ( "\n", "" )
        foundLine = False
        with open(self.fileName, "r") as f:
            lines = f.readlines()
        with open(self.fileName, "w") as f:
            for line in lines:
                if line.strip("\n") != link:
                    f.write(line)
                else:
                    foundLine = True
                    
        if foundLine != True:
            print(line)
            raise IOError('succ')

    def swapLine(self, oldLine, newLine):
        self.excludeLine(oldLine)
        self.appendToFile(newLine)






