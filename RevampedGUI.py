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
root.geometry("600x400")
root.resizable(0,0)

#btn style
btnstyle = ttk.Style().configure("my.TButton", font=("mont",))


#radiobtn style
radioStyle = ttk.Style().configure("my.TRadiobutton", font=("mont",))

#textvariable data of buttons is stored here        
nameData = StringVar()
uidData = StringVar()
candData = StringVar()

def openAdminWin():
    global btnstyle
    global adminWinLabel
    global voterOpBtn 
    global candidateOpBtn
    global setVoteSessionBtn
    global startVoterSessionBtn
    global adminSettingBtn
    global adminLogoutBtn

    adminWinLabel = ttk.Label(root, text="Welcome Admin", font="mont")
    voterOpBtn = ttk.Button(root, text="Configure Voters' List", style="my.TButton")
    candidateOpBtn = ttk.Button(root, text="Configure Candidates' List", style="my.TButton")
    setVoteSessionBtn = ttk.Button(root, text="Setup Voting Session", style="my.TButton")
    startVoterSessionBtn = ttk.Button(root, text="Start a Voting Session", style="my.TButton", padding=(25,3,25,3))
    adminSettingBtn = ttk.Button(root, text="Admin Settings", style="my.TButton")
    adminLogoutBtn = ttk.Button(root, text="Logout", style="my.TButton", padding=(20,3,20,3), command=adminLogout)

    adminWinLabel.grid(row=0, column=0, columnspan=2, pady=(10,0), padx=(110,0))
    voterOpBtn.grid(row=1, column=0, padx=(10,5), pady=(10,10))
    candidateOpBtn.grid(row=1, column=1, padx=(10,5), pady=(10,10))
    setVoteSessionBtn.grid(row=2, column=0, padx=(10,5), pady=(10,10))
    startVoterSessionBtn.grid(row=2, column=1, padx=(10,5), pady=(10,10))
    adminSettingBtn.grid(row=3, column=0, padx=(10,5), pady=(10,10), columnspan=2)
    adminLogoutBtn.grid(row=4, column=0, padx=(10,5), pady=(10,10), columnspan=2)

def adminLogout():
    adminWinLabel.grid_remove()
    voterOpBtn .grid_remove()
    candidateOpBtn.grid_remove()
    setVoteSessionBtn.grid_remove()
    startVoterSessionBtn.grid_remove()
    adminSettingBtn.grid_remove()
    adminLogoutBtn.grid_remove()
    showMainWidgets()

def openDebugWin():
    global btnstyle
    global debugWin
    debugWin = Toplevel()
    debugWin.title("Debug Operations")
    consoleVoterListBtn = ttk.Button(debugWin, text="Voter List", command=display_voters_debug, style="my.TButton").grid(row=0, column=0, padx=15, ipadx=35, pady=15)
    consoleCandidateListBtn = ttk.Button(debugWin, text="Candidate List", command=display_candidates_debug, style="my.TButton").grid(row=1, column=0, ipadx=30, pady=15)
    hideallWidgets = ttk.Button(debugWin, text="Hide all Widgets", command=hideMainWidgets, style="my.TButton").grid(row=2, column=0, pady=15, padx=15)

def showMainWidgets():
    nameLabel.grid(row=0, column=0, sticky=W, padx=(110,30), pady=(130,0))
    nameEntry.grid(row=0, column=1, padx=(15,90), pady=(130,0))
    passLabel.grid(row=1, column=0, sticky=W, padx=(110,0), pady=(20,0))
    passEntry.grid(row=1, column=1, padx=(15,90), pady=(20,0))
    submitbtn.grid(row=2, column=0, columnspan=2, pady=(30,0))
    loginErrorLabel.grid(row=3, column=0, pady=(15,15), columnspan=2)
    loginErrorLabel.grid_remove()

def hideMainWidgets():
    global nameLabel
    global nameEntry
    global passLabel
    global passEntry
    global submitbtn
    nameLabel.grid_remove()
    nameEntry.grid_remove()
    passLabel.grid_remove()
    passEntry.grid_remove()
    submitbtn.grid_remove()
    loginErrorLabel.grid_remove()
    

def submitOnClick(event = None):
    hideMainWidgets()
    global getName
    getName = nameData.get()
    getUID = uidData.get()
    
    loginErrorLabel.grid_remove()
    adminListDAT = open("Data/cred.dat", "rb")
    found = 0
    try:
        while True:
            dataAdmin = pickle.load(adminListDAT)
            if getName == caesarCipher.caesarDecrypt(dataAdmin["Admin Name"]) and getUID == caesarCipher.caesarDecrypt(dataAdmin["Password"]):
                found = 1
                break
    except EOFError:
        adminListDAT.close()
    if found == 1:
        loginErrorLabel.grid_remove()
        openAdminWin()
    else:
        showMainWidgets()
        loginErrorLabel.grid()


root.bind("<Return>", submitOnClick)

#main window widgets
nameLabel = ttk.Label(root, text="Enter your name:", font="mont")
nameEntry = ttk.Entry(root, font="mont", textvariable=nameData)
passLabel = ttk.Label(root, text="Enter your Password:", font="mont")
passEntry = ttk.Entry(root, font="mont", textvariable=uidData, show="*")
submitbtn = ttk.Button(root, text="Login",command=submitOnClick, style="my.TButton")
loginErrorLabel = ttk.Label(root, font="mont", text="Sorry but it seems like\nyou aren't in the Voters' List!", justify=CENTER)

openDebugWin()
showMainWidgets()
root.mainloop()
