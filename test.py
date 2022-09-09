from tkinter import *
from tkinter import ttk
from helper import *
from eAuth import *
from modify import *
from election import *


#main window
root = Tk()
root.title("Election App Mockup")
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")

mainFrame = ttk.Frame(root, width=600, height=400).grid(row=0,column=0)

root.mainloop()