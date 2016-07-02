from tkinter import *
import threading
from GUIlib import *

class connectionWindow():
    def __init__(self, host, serverName, handler):
        
        self.root = Tk() 
        self.root.bind("<Return>", lambda event: self.appendTextDisplay())
        self.root.bind("<End>", lambda event: self.clearAll())
        self.root.bind("<Escape>", lambda event: self.shutDownConnection())
        self.root.bind("<Button-1>", lambda event: self.inputBar.focus_set())
        self.root.bind("<Alt_L>", lambda event: self.displayHelpWindow())
        self.root.maxsize(width= 400, height= 500)
        self.root.resizable(width= FALSE, height= FALSE)
        self.root.wm_title("           Server: " + serverName + "     IP: " + str(host))
        self.root.protocol('WM_DELETE_WINDOW', lambda: self.shutDownConnection());
        
        self.handler = handler

        self.textFrame = Frame(self.root, width= 100)
        self.textFrame.pack(side= TOP)
        self.inputFrame = Frame(self.root, width= 100)
        self.inputFrame.pack()
        self.buttonFrame = Frame(self.root, width= 100)
        self.buttonFrame.pack(side= BOTTOM)

        self.textDisplay = Text(self.textFrame, relief= RAISED, background= "black", foreground= "green", wrap= WORD)
        self.yScrollBar = Scrollbar(self.textFrame, command= self.textDisplay.yview, relief= "sunken")
        self.textDisplay['yscrollcommand'] = self.yScrollBar.set
        self.yScrollBar.pack(side= RIGHT, fill= Y)
        self.textDisplay.config(state= DISABLED)
        self.textDisplay.pack()

        self.menu = Menu(self.root)
        addHelpMenu(self.menu)
        addColorMenu(self.menu, self.textDisplay)
        self.root.config(menu= self.menu)

        self.inputBar = Entry(self.inputFrame, bd= 5, width= 42)
        self.inputBar.pack(side= LEFT, fill= X)
        self.inputButton = Button(self.inputFrame, text= "Enter", command= self.appendTextDisplay)
        self.clearButton = Button(self.inputFrame, text= "Clear", command= self.clearAll)
        self.clearButton.pack(side= RIGHT)
        self.inputButton.bind("<Return>", self.appendTextDisplay)
        self.inputButton.pack(side= RIGHT)
        
        self.displayButton = Button(self.buttonFrame, text= "Display Connections", command= self.displayConnections)
        self.displayButton.pack(side= LEFT, fill= X)
        self.changeButton = Button(self.buttonFrame, text= "Change Connection", command= lambda: displayInputWindow(["New Connection Number: "], self.changeActiveConnection))
        self.changeButton.pack(side = LEFT, fill= X)
        self.closeButton = Button(self.buttonFrame, text= "Close Connection", command= self.closeActiveConnection)
        self.closeButton.pack(side= LEFT, fill= X)

        self.inputBar.focus_set()
        self.root.mainloop()

    def appendTextDisplay(self):
        self.textDisplay.config(state= "normal")
        self.textDisplay.insert(INSERT, "\n" + self.inputBar.get())
        self.inputBar.delete(0, END)
        self.textDisplay.config(state= DISABLED)
        self.textDisplay.see(END)

    def clearAll(self):
        self.textDisplay.config(state= "normal")
        self.textDisplay.delete(1.0, END)
        self.textDisplay.config(state= DISABLED)

    def changeActiveConnection(newConNum):
        self.socket = self.server.connections[newConNum][0]
        self.clearAll()
        self.showMessage("Starting new connection with: " + str(self.server.connections[newConNum][1]))

    def closeActiveConnection(self):
        self.handler.socket.close()
        self.handler.end()
        
    def shutDownConnection(self):
        self.handler.exit()
        self.root.destroy()

if __name__ == "__main__":
    con1 = threading.Thread(target= connectionWindow, args= ("1"))
    con1.start()
    con2 = threading.Thread(target= connectionWindow, args= ("2"))
    con2.start()
    con3 = threading.Thread(target= connectionWindow, args= ("3"))
    con3.start()
