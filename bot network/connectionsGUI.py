import threading
import os
import time
from tkinter import *
from GUItesting import *
from GUIlib import *

class serverGUI():

    def __init__(self, host, port, serverName, server):
        self.host = host
        self.port = int(port)
        self.serverName = serverName
        self.server = server

        self.printLock = threading.Lock()
        self.displayLock = threading.Lock()

        self.root = Tk()
        self.root.resizable(width= FALSE, height= FALSE)
        self.root.wm_title("Botnetwork Server: " + serverName)
        self.root.bind("<Return>", lambda event: self.appendConsole())
        self.root.bind("<Escape>", lambda event: self.toggleServer())
        self.root.bind("<End>", lambda event: self.clearAll())
        self.root.bind("<Button-1>", lambda event: self.inputBar.focus_set())
        self.root.bind("<Alt_L>", lambda event: displayHelpWindow())
        self.root.protocol('WM_DELETE_WINDOW', lambda: self.shutDownServer());
        
        self.menu = Menu(self.root)
        self.root.config(menu= self.menu)
        self.textDisplayFrame = Frame(self.root, width= 700, height= 500)
        self.textDisplayFrame.pack()
        self.messageFrame = Frame(self.root)
        self.messageFrame.pack(side= LEFT, anchor= S)
        self.buttonFrame = Frame(self.root, width= 800, height= 50)
        self.buttonFrame.pack(side= BOTTOM)
        self.inputFrame = Frame(self.root, width= 30)
        self.inputFrame.pack(side= BOTTOM)


        self.connectionScreen = Text(self.textDisplayFrame, width= 50, relief= RAISED)
        self.connectionScroll = Scrollbar(self.textDisplayFrame, command= self.connectionScreen.yview, relief= "sunken")
        self.connectionScreen['yscrollcommand'] = self.connectionScroll.set
        self.connectionScreen.pack(side= LEFT)
        self.connectionScreen.config(highlightbackground= "black", highlightthickness= 1)
        self.connectionScroll.pack(side= LEFT, fill= Y)
        self.consoleScreen = Text(self.textDisplayFrame, width= 50, relief= RAISED, background= "black", foreground= "green")
        self.consoleScreen.config(state= DISABLED)
        self.consoleScroll = Scrollbar(self.textDisplayFrame, command= self.consoleScreen.yview, relief= "sunken")
        self.consoleScreen['yscrollcommand'] = self.consoleScroll.set
        self.consoleScroll.pack(side = RIGHT, fill= Y)
        self.consoleScreen.pack(side= RIGHT)

        addHelpMenu(self.menu)
        addColorMenu(self.menu, self.connectionScreen, "Display Colors")
        addColorMenu(self.menu, self.consoleScreen, "Console Colors")
        self.options= Menu(self.menu)
        self.menu.add_cascade(label= "Options", menu= self.options)
        addSetterMenu(self.options, ["Host IP ", "Host Port ", "Backlog Limit ", "Host Name "], [self.changeHost, self.changePort, self.changeBacklogs, self.changeServerName])
        
        self.inputBar = Entry(self.inputFrame, width= 66, bd= 5)
        self.clearButton = Button(self.inputFrame, text= "Clear", command= self.clearAll)
        self.clearButton.pack(side= RIGHT)
        self.enterButton = Button(self.inputFrame, text= "Enter", command= self.appendConsole)
        self.enterButton.pack(side= RIGHT)
        self.inputBar.pack(side= RIGHT, fill= X)
        self.lastMessage = None

        self.portLabel = Label(self.messageFrame, text= "Host Port: " + str(self.port))
        self.portLabel.pack(side= BOTTOM, anchor= W)
        self.hostLabel = Label(self.messageFrame, text= "Host IP: " + str(self.host))
        self.hostLabel.pack(side= BOTTOM, anchor= W)
        self.totalConsLabel = Label(self.messageFrame, text= "Total Connections: " + str(0))
        self.totalConsLabel.pack(side= LEFT, anchor= NW)
        
        self.closeAllButton = Button(self.buttonFrame, text= "Close All Connections", command= lambda: self.server.closeConnections(), bd= 3)
        self.closeAllButton.pack(side= RIGHT, padx= 2)
        self.toggleServerButton = Button(self.buttonFrame, text= "Pause", command= self.toggleServer, bd= 3)        
        self.toggleServerButton.pack(side= RIGHT, padx= 2)
        self.newServerButton = Button(self.buttonFrame, text= "New Server", bd= 3, command= lambda: displayInputWindow(["New Server IP: ", "New Server Port: ", "New Server Backlogs: ", "New Server Name: "], self.createNewServer))
        self.newServerButton.pack(side= RIGHT, padx= 2)
        self.newWindowButton = Button(self.buttonFrame, text= "New Connection Window", bd= 3, command= lambda: displayInputWindow(["Connection Number: "], self.createCon))
        self.newWindowButton.pack(side= RIGHT, padx= 2)
        self.quitButton = Button(self.buttonFrame, text= "Quit", bd= 3, command= lambda: self.shutDownServer())
        self.quitButton.pack(side= RIGHT, padx= 2)
        self.helpButton = Button(self.buttonFrame, text= "Help", bd= 3, command= displayHelpWindow)
        self.helpButton.pack(side= RIGHT, padx= 2)

        self.connectionsThread = threading.Thread(target= self.displayConnections)
        self.connectionsThread.start()
        
        self.root.mainloop()

    def appendConsole(self, msg= None):
        self.printLock.acquire()
        self.consoleScreen.config(state= "normal")
        if msg is None:
            self.consoleScreen.insert(INSERT, self.inputBar.get() + "\n")
            self.lastMessage = self.inputBar.get()
            self.inputBar.delete(0, 'end')
        else:
            if msg == ">>" or msg == "\n>>":
                self.console.insert(INSERT, msg)
            else:    
                self.consoleScreen.insert(INSERT, msg + "\n")
            
        self.consoleScreen.see(END)
        self.consoleScreen.config(state= DISABLED)
        self.printLock.release()

    def displayConnections(self):
        while True:
            self.displayLock.acquire()
            self.connectionScreen.config(state= "normal")
            self.connectionScreen.delete(1.0, END)
            for conNum in range(len(self.server.connections)):
                self.connectionScreen.insert(INSERT, str(conNum + 1) + ". IP: " + str(self.server.connections[conNum][1]))
            self.connectionScreen.config(state= DISABLED)
            time.sleep(3)
            self.displayLock.release()
    
    def clearAll(self):
        self.consoleScreen.config(state= "normal")
        self.consoleScreen.delete(1.0, END)
        self.consoleScreen.config(state= DISABLED)

    def toggleServer(self):
        if self.toggleServerButton.config('text')[-1] == "Pause":
            if self.server.closeServer():
                self.toggleServerButton.config(text= "Unpause")
            
        else:
            if self.server.openServer():
                self.toggleServerButton.config(text= "Pause")

    def isServerActive(self):      
            if self.toggleServerButton.config('text')[-1] == "Pause":
                return True
            else:
                return False
            
    def shutDownServer(self):
        if self.server.socket is not None:
            self.server.socket.close()
        self.server.end()
        self.root.destroy()
        
    def createNewServer(self, entries):
        os.system("serverBot -ho " + str(entries[0]) + " -p " + str(entries[1]) + "-b " + str(entries[2]) + " -sn " + str(entries[3]))
        #server = serverBot(entries[0], entries[1], entries[2], entries[3])
        #super(serverBot, server).__init__()
        #server.start()
        
    def createCon(self, conNum):
        ip = self.server.connections[conNum]
        botHandler(ip[0], self.server)
        botHandler.start()

    def changeHost(self, newHost):
        if self.isServerActive():
            self.server.closeServer()

        self.host = newHost
        self.server.host = newHost
        self.hostLabel.config(text= newHost)

        if self.isServerActive():
            self.server.openServer()
    
    def changePort(self, newPort):
        if self.isServerActive():
            self.server.closeServer()
            
        self.port = port
        self.server.port = newPort
        self.portLabel.config(text= newPort)

        if not self.isServerActive():
            self.server.openServer()

    def changeBacklogs(self, newBacklogs):
        if self.isServerActive():
            self.server.closeServer()
            
        self.server.backlogs = newBacklogs
        
        if not self.isServerActive():
            self.server.openServer()
    
    def changeServerName(self, newName):
        if self.isServerActive():
            self.server.closeServer()
            
        self.serverName = newName
        self.server.serverName = newName
        self.root.wm_title("Botnetwork Server: " + newName)

        if not self.isServerActive():
            self.server.openServer()
    
if __name__ == "__main__":
    GUI = serverGUI("127.0.0.1", 5000, "Root Server", None)
