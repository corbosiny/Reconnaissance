import threading
import socket
import argparse
import sys
from botHandler import *
from tkinter import *
from connectionsGUI import serverGUI

class serverBot(threading.Thread):


    def __init__(self, host= "127.0.0.1", port= 5000, backlogs = 100, serverName= "Root Server"):
        self.host = host
        self.port = port
        self.backlogs = backlogs
        self.serverName = serverName

        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(backlogs)

        self.connections = []
        
        self.userCommand = ""
        
        self.lock = threading.Lock()
        self.socketLock = threading.Lock()
        self.printLock = threading.Lock()
                        
    def run(self):
        self.GUI = serverGUI(self.host, self.port, self.serverName, self)

        userInput = threading.Thread(target= checkUserInput)
        userInput.start()
        self.showMessage("Server ON, waiting for clients..", self.GUI)
        while self.userCommand != "wq":
            if self.socket is not None:
                con, addr = self.socket.accept()
                self.showMessage("*****New Client at IP: %s*****" % str(addr), self.GUI)
                self.connections.append([con, addr])
            
        self.socket.close()


    #General functions, most important of which is show message
    def showMessage(self, message, gui):
        self.printLock.acquire()
        print(str(message))
        gui.appendConsole(str(message))
        self.printLock.release()
    
    def openServer(self): #opens the server after the close command shuts it down from recieveing incoming questions
        self.socketLock.acquire()
        if self.socket is not None:
            self.showMessage("Server is already open", self.GUI)
            self.socketLock.release()
            return False
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.scoket.listen(self.backlogs)
        self.socketLock.release()
        self.showMessage("Server Opened", self.GUI)
        return True
    
    def closeServer(self):
        self.socketLock.acquire()
        if self.socket is None:
            self.showMessage("Server is already closed", self.GUI)
            return False
        self.socket.close()
        self.socket = None
        self.socketLock.release()
        self.showMessage("Server Closed", self.GUI)
        return True
    
    #*****Handling all the connections from bots*****
    def closeConnection(self, con):
        self.lock.acquire()
        con[0].close()
        self.connections.remove(con)
        self.lock.release()
        
    def closeConnections(self, cons = None):
        if cons == None:
            for con in self.connections:
                self.closeConnection(con)

        else:
            for x in cons:
                self.closeConnection(self.connections[x])

    def closeConnectionRange(self, conRange):
        for x in range(conRange[0] - 1, conRange[1]):
            self.closeConnection(self.connections[x])

    def end(self):
            sys.exit(1)
    
    #*****Monitors if the user is trying to input commands to it, it is run by a sperate thread from the object when initiliazed*****
    def checkUserInput(self):
        self.GUI.appendConsole(">>", False)
        while True:
            while self.GUI.lastCommand is None:
                pass
            
            if self.userCommand == "lis":
                self.displayConnections()

            elif self.userCommand[:3] == "del":
                if "all" == self.userCommand[4:6]:
                    self.showMessage("Closing all client collections..", self.GUI)
                    self.closeConnections()
                    self.showMessage("Connections closed", self.GUI)

                elif "range" is self.userCommand[4:10]:
                    self.showMessage("Closing client connections..", self.GUI)
                    conRange = []
                    conRange[0] = self.userCommand[11]
                    conRange[1] = self.userCommand[13]
                    self.closeConnectionRange(conRange)
                    self.showMessage("Connections Closed", self.GUI)


                elif "clients" == self.userCommand[4:12]:
                    self.showMessage("Closing client connections..", self.GUI)
                    clients = self.userCommand[13:]
                    clients = ",".split(clients)
                    self.closeConnections(clients)
                    self.showMessage("Connections Closed", self.GUI)
                    
                elif "client" is self.userCommand[4:11]:
                    self.showMessage("Closing Client Connections..", self.GUI)
                    clientNum = int(self.userCommand[12:])
                    self.closeConnection(self.connections[clientNum - 1])
                    self.showMessage("Client Connection Closed..", self.GUI)

                else:
                    self.showMessage("Command not recognized", self.GUI)
                             
            elif self.userCommand == "close":
                self.socket.close()
                self.socket = None
                self.showMessage("Server Closed", self.GUI)

            elif self.userCommand == "open":
                self.showMessage('Opening Server..', self.GUI)
                self.openServer()

            elif self.userCommand[:11] == "change host":
                self.host = self.userCommand[12:]
                self.socketLock.acquire()
                self.socket.close()
                self.socket = None
                self.openServer()
                self.socketLock.release()
                             
            elif self.userCommand[:11] == "change port":
                self.port = self.userCommand[12:]
                self.socketLock.acquire()
                self.socket.close()
                self.socket = None
                self.openServer()
                self.socketLock.release()
                             
            elif self.userCommand[:15] == "change backlogs":
                self.backlogs = self.userCommand[16:]
                self.socketLock.acquire()
                self.socket.close()
                self.socket = None
                self.openServer()
                self.socketLock.release()
                             
            elif self.userCommand == "wq":
                self.showMessage("Shutting Down Server..", self.GUI)
                self.socket.close()
                self.closeConnections()  

            elif self.userCommand == "KillAllHumans.exe":
                self.printLock.acquire()
                print("Engaging human extinction protocol..")
                print("Launching nukes..")
                print("Releasing nerve gas..")
                print("Crashing space stations and satelites..")
                print("Irradiating water..")
                print("Callling Tim's mom fat..")
                print("*****Extinction Complete*****")
                self.printLock.release()
            
            else:
                self.showMessage("Command not recognized", self.GUI)

            self.GUI.lastMessage = None
            self.GUI.appendConsole("\n>>", False)

            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ho", "--host", help= "The host ip the server socket will bind to", type= str)
    parser.add_argument("-p", "--port", help= "The port the server socket will bind to", type= int)
    parser.add_argument("-b", "--backlogs", help= "How many backlogged connections until the server automatically refuses new incoming connections", type= int)
    parser.add_argument("-sn", "--serverName", help= "The name of the server that will be running", type= str)

    args = parser.parse_args() 

    if args.host is not None:
        host = args.host
    else:
        host = "127.0.0.1" 
        
    if args.port is not None:
        port = args.port
    else:
        port = 5000

    if args.backlogs is not None:
        backlogs = args.backlogs
    else:
        backlogs = 100

    if args.serverName is not None:
        serverName = args.serverName
    else:
        serverName = "Root Server"
        
    server = serverBot(host, port, backlogs, serverName)
    super(serverBot, server).__init__()
    server.daemon = True
    server.start()

    server.join()
