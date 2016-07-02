import threading, socket, argparse, sys, os, serverBot


class botHandler(threading.Thread):
    def __init__(self, con, server):
        
        self.server = server
        self.host = self.server.host
        self.serverName = self.server.serverName
        self.connectionGUI = connectionWindow(self.host, self.serverName, self)
        self.socket = con

        self.lock = threading.Lock()
        self.printLock = threading.Lock()

    def showMessage(message):
        self.printLock.acquire()
        print(str(message))
        self.appendTextDisplay(message)
        self.printLock.release()

    #*****How the user will interact with this connection*****
    def sendCommands(self): 
        if not isActive:
            return False

        command = ""
        cwd = ""
        while command is not 'wq':
            try:
                command = str(input(cwd + ">>"))
                self.activeConnection[0].sendData(command)
                if command[0] is "@":
                    if command[1:8] == "recieve":
                        if command[9:12] == "dir":
                            response = self.activeConnection[0].recieveData()
                            if response == "OK":
                                self.sendDir(command[13:])
                            else:
                                self.showMessage("Error in recieving comand, check spelling")
                                continue
                        if command[9:14] == "files":
                            response = self.activeConnection[0].recieveData()
                            if response == "OK":
                                fileNames = command[15:]
                                names = ",".split(fileNames)
                                self.returnFiles(names)

                            else:
                                self.showMessage("Error in recieving command, check spelling")
                                continue
                            
                        if command[9:13] == "file":
                            response = self.activeConnection[0].recieveData()
                            if respone == "OK":
                                self.sendFile(command[14:])
                            else:
                                self.showMessage("Error in recieving command, check spelling")
                                continue

                    elif command[1:7] == "return":
                        if command[8:11] == "dir":
                            respone = self.activeConnection[0].recieveData()
                            if response == "OK":
                                self.sendData("OK")
                                self.sendData(str(input("Clearence: ")))
                                self.recieveDir(command[12:])
                            else:
                                self.showMessage("Error in recieving command, check spelling")
                                continue
                        elif command [8:13] == "files":
                            response = self.activeConnection[0].recieveData()
                            if response == "OK":
                                fileNames = command[14:]
                                names = ",".split(fileNames)
                                recieveFiles(names)

                            else:
                                self.showMessage("Error in recieving command, check spelling")
                                continue
                        elif command[8:12] == "file":
                            respone = self.activeConnection[0].recieveData()
                            if response == "OK":
                                self.recieveData(command[13:])
                            else:
                                self.showMessage("Error in recieving command, check spelling")
                                continue
                else:
                    response = self.activeConnection[0].recieveData()
                    showMessage(response)
                       
                cwd = self.activeConnection[0].recieveData()
                
            except:
                self.showMessage("Error with socket connection, closing connection")
                self.closeActiveConection()

    

    #*****sending and recieving all types of data, files, and whole directories*****
    def isError(data):
        if "$ERROR$" in data[-6:]:
            return True
        else:
            return False
        
    def sendData(self, data, binary= False, size= None):
        if size is None:
            size = str(sys.getsize(data)).zfill(1024)
        try:
            self.activeConnection[0].send(str(size).encode('utf-8'))
            if not binary:
                self.activeConnection[0].send((str(0).zfill(1024)).encode('utf-8'))
                self.activeConnection[0].send(data.encode('utf-8'))
            else:
                self.activeConnection[0].send((str(1).zfill(1024)).encode('utf-8'))
                self.activeConnection[0].send(data)
            return True
        
        except:
            self.activeConnection[0].send("$ERROR$".zfill(int(size)))
            return False

    def recieveData(self, fileName = None):
        size = self.activeConnection[0].recv(1024).decode('utf-8')
        binary = self.activeConnection[0].recv(1024).decode('utf-8')
        if binary == "1":
            binary = True
        else:
            binary = False
            
        data = self.activeConnection[0].recv(int(size))
        if isError(size) or (isError(binary) or isError(data)):
            self.showMessage("An error was encountered sending the data, check if the data or file being sent exist")
    
                                                 
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

            else:
              break
            
    def returnFile(self, path):
        if not 'C:' in path:
            path = os.path.join(path, os.getcwd)
            
        with open(path, 'rb') as file:
            data = file.read()
            self.sendData(data, True)
            
            file.close()

    def returnFiles(self, fileNames):
        for file in fileNames:
            self.returnFile(file)
        
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
                returnFile(path)
           elif os.path.isdir(path) and clearance != 0:
                directories.append(path)

           else:
                pass
            
        if clearence != 0:
            for direc in directories:
                path = os.path.join(direc, directory)
                self.socket.send("NEW DIRECTORY: " + direc)
                self.returnDirectory(path, clearance - 1, False)

        self.sendData('__DONE__')        

    def run(self):
        self.sendCommands()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ho", "--host", help= "The host ip the server socket will bind to", type= str)
    parser.add_argument("-p", "--port", help= "The port the server socket will bind to", type = int)
    parser.add_argument("-b", "--backlogs", help= "How many backlogged connections until the server automatically refuses new incoming connections", type= int)

    args = parser.parse_args()

    print("Running server on IP: %s and port: %d") % args.host, args.port

    if args.host:
        host = args.host
    else:
        host = "127.0.0.1" 
        
    if args.port:
        port = args.port
    else:
        port = 5000
        
    if args.backlogs:
        backlogs = args.backlogs
    else:
        backlogs = 100

    handler.start()
    handler.join()
