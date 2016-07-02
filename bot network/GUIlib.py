from tkinter import *
import functools

def addHelpMenu(menu, name= "Help", msg= "Help Screen"):
    menu.add_command(label= name, command= lambda: displayHelpWindow(msg))

def displayMessageWindow(title, msg):
    window = Toplevel()
    window.bind("<Return>", lambda event: window.destroy())
    window.bind("<Escape>", lambda event: window.destroy())
    window.title(title)
    label= Label(window, text= str(msg))
    label.pack(side= TOP)
    window.focus_force()
    
def displayHelpWindow(msg= "Help Screen", title= "Help"):
    displayMessageWindow(title, msg)

def addColorMenu(menu, display, name= "Colors"):
        subMenu = Menu(menu)
        menu.add_cascade(label= name, menu= subMenu)
        bgMenu = Menu(subMenu)
        bgMenu.add_command(label= "Blue", command= lambda: changeBG("blue", display))
        bgMenu.add_command(label= "Green", command= lambda: changeBG("green", display))
        bgMenu.add_command(label= "Red", command= lambda: changeBG("red", display))
        bgMenu.add_command(label= "Grey", command= lambda: changeBG("grey", display))
        bgMenu.add_command(label= "Black", command= lambda: changeBG("black", display))
        bgMenu.add_command(label= "Yellow", command= lambda: changeBG("yellow", display))
        bgMenu.add_command(label= "Pink", command= lambda: changeBG("pink", display))
        bgMenu.add_command(label= "Purple", command= lambda: changeBG("purple", display))
        bgMenu.add_command(label= "White", command= lambda: changeBG("white", display))
        bgMenu.add_command(label= "Magenta", command= lambda: changeBG("magenta", display))
        bgMenu.add_command(label= "Cyan", command= lambda: changeBG("cyan", display))
        bgMenu.add_command(label= "Custom", command= lambda: customColor(1, display))
        colorMenu = Menu(subMenu)
        colorMenu.add_command(label= "Blue", command= lambda: changeFG("blue", display))
        colorMenu.add_command(label= "Green", command= lambda: changeFG("green", display))
        colorMenu.add_command(label= "Red", command= lambda: changeFG("red", display))
        colorMenu.add_command(label= "Grey", command= lambda: changeFG("grey", display))
        colorMenu.add_command(label= "Black", command= lambda: changeFG("black", display))
        colorMenu.add_command(label= "Yellow", command= lambda: changeFG("yellow", display))
        colorMenu.add_command(label= "Orange", command= lambda: changeFG("orange", display))
        colorMenu.add_command(label= "Pink", command= lambda: changeFG("pink", display))
        colorMenu.add_command(label= "Purple", command= lambda: changeFG("purple", display))
        colorMenu.add_command(label= "White", command= lambda: changeFG("white", display))
        colorMenu.add_command(label= "Magenta", command= lambda: changeFG("magenta", display))
        colorMenu.add_command(label= "Cyan", command= lambda: changeFG("cyan", display))
        colorMenu.add_command(label= "Custom", command= lambda: customColor(2, display))
        subMenu.add_cascade(label= "Background Colors:", menu= bgMenu)
        subMenu.add_cascade(label= "Text Colors:", menu= colorMenu)
        subMenu.add_separator()


def changeBG(color, display):
    display.config(background= color)

def changeFG(color, display):
    display.config(foreground= color)

def changeColor(color, num, display):
    if num == 1:
        changeBG(color, display) 
    else:
        changeFG(color, display)

def customColor(num, display):
    inputWindow = Toplevel()
    inputWindow.bind("<Return>", lambda event: changeColor(inputBar.get(), var.get(), display))
    inputWindow.bind("<Escape>", lambda event: inputWindow.destroy())
    inputWindow.bind("<Button-1>", lambda event: inputBar.focus_set())
    inputFrame = Frame(inputWindow)
    inputFrame.pack(side= TOP)
    radioButtonFrame = Frame(inputWindow)
    radioButtonFrame.pack(side= TOP)
    var = IntVar()
    radio1 = Radiobutton(radioButtonFrame, variable= var, text= "BG", value= 1)
    radio1.pack(side= LEFT)
    radio2 = Radiobutton(radioButtonFrame, variable= var, text= "FG", value= 2)
    radio2.pack(side= LEFT)
    if num == 1:
        radio1.invoke()
        radio2.deselect()
    else:
        radio2.invoke()
        radio1.deselect()
    inputBar = Entry(inputFrame)
    inputBar.pack(side= LEFT)
    inputButton = Button(inputFrame, text= "Enter", command= lambda: changeColor(inputBar.get(), var.get(), display))
    inputButton.pack(side= LEFT)
    label1 = Label(inputWindow, text= "EX: #000000000, black")
    label1.pack(side= BOTTOM)
    label2 = Label(inputWindow, text= "Enter a custom color in Hexadecimal form")
    label2.pack(side= BOTTOM)
    inputWindow.focus_force()
    inputBar.focus_set()

def displayInputWindow(labels, targetFunction):
    entries = []
    displayWindow = Toplevel()
    displayWindow.focus_set()
    displayWindow.bind("<Escape>", lambda event: displayWindow.destroy())
    for x in labels:
        label = Label(displayWindow, text= x + ":")
        label.pack(side= TOP)
        entry = Entry(displayWindow)
        entry.pack(side= TOP)
        entries.append(entry)
        if labels.index(x) == 0:
            entry.focus_set()
    
    but = Button(displayWindow, text= "Enter", command= lambda: getInputs(entries, targetFunction, displayWindow))
    but.pack(side= BOTTOM)
    displayWindow.bind("<Return>", lambda event: getInputs(entries, targetFunction, displayWindow))
    
def getInputs(entries, targetFunction, window):
    inputs = []
    for entry in entries:
        inputs.append(entry.get())
    window.destroy()
    targetFunction(inputs)

def addSetterMenu(menu, labels, targetFunctions, separator= True):
    for x in range(len(labels)):
        menu.add_command(label= labels[x], command=functools.partial(displayInputWindow, [labels[x]], targetFunctions[x]))

    if separator:
        menu.add_separator()
