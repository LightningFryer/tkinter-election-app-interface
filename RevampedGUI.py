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

#btn style
btnstyle = ttk.Style().configure("my.TButton", font=("mont",))


#radiobtn style
radioStyle = ttk.Style().configure("my.TRadiobutton", font=("mont",))

#textvariable data of buttons is stored here        
nameData = StringVar()
uidData = StringVar()
candData = StringVar()

# def castOnClick():
#     voterWinLabel.destroy()

# def openVoterWin():
#     global btnstyle
#     global voterWin
#     voterWin = Toplevel()
#     voterWin.title("Cast your vote!")
#     voterWinLabel = ttk.Label(voterWin, text="Cast your vote using by clicking\none of the voter names below", justify="center", font="mont").grid(row=0, column=0, columnspan=2, padx=15, pady=15)
#     castVoteBtn = ttk.Button(voterWin, text="Cast my vote!", style="my.TButton").grid(row=4, column=0, columnspan=2, pady=15)
#     candOne = ttk.Radiobutton(voterWin, text="Candidate One",style="my.TRadiobutton", variable=candData, value=1).grid(row=2, column=0, padx=(15,0), sticky=W)
#     candTwo = ttk.Radiobutton(voterWin, text="Candidate Two",style="my.TRadiobutton", variable=candData, value=2).grid(row=2, column=1, padx=(0, 15))
#     candThree = ttk.Radiobutton(voterWin, text="Candidate Three",style="my.TRadiobutton", variable=candData, value=3).grid(row=3, column=0, padx=(15,0))
#     candFour = ttk.Radiobutton(voterWin, text="Candidate Four",style="my.TRadiobutton", variable=candData, value=4).grid(row=3, column=1, padx=(0,15))
#     # voterWinSep = ttk.Separator(voterWin, orient=HORIZONTAL).grid(row=1, column=0, sticky=EW, columnspan=2) #Doesn't look good imo

def openAdminWin():
    global btnstyle
    global adminWin
    adminWin = Toplevel()
    adminWin.title("Admin Controls Panel")
    adminWinLabel = ttk.Label(adminWin, text="Welcome Admin", font="mont").grid(row=0, column=0, columnspan=2, pady=(10,0))
    voterOpBtn = ttk.Button(adminWin, text="Configure Voters' List", style="my.TButton").grid(row=1, column=0, padx=(10,5), pady=(10,10))
    candidateOpBtn = ttk.Button(adminWin, text="Configure Candidates' List", style="my.TButton").grid(row=1, column=1, padx=(10,5), pady=(10,10))
    setVoteSessionBtn = ttk.Button(adminWin, text="Setup Voting Session", style="my.TButton").grid(row=2, column=0, padx=(10,5), pady=(10,10))
    startVoterSessionBtn = ttk.Button(adminWin, text="Start a Voting Session", style="my.TButton", padding=(25,3,25,3)).grid(row=2, column=1, padx=(10,5), pady=(10,10))
    adminSettingBtn = ttk.Button(adminWin, text="Admin Settings", style="my.TButton").grid(row=3, column=0, padx=(10,5), pady=(10,10), columnspan=2)
    adminLogoutBtn = ttk.Button(adminWin, text="Logout", style="my.TButton", padding=(20,3,20,3), command=adminWin.destroy).grid(row=4, column=0, padx=(10,5), pady=(10,10), columnspan=2)

def openDebugWin():
    global btnstyle
    global debugWin
    debugWin = Toplevel()
    debugWin.title("Debug Operations")
    consoleVoterListBtn = ttk.Button(debugWin, text="Voter List", command=display_voters_debug, style="my.TButton").grid(row=0, column=0, padx=15, ipadx=35, pady=15)
    consoleCandidateListBtn = ttk.Button(debugWin, text="Candidate List", command=display_candidates_debug, style="my.TButton").grid(row=1, column=0, ipadx=30, pady=15)

def submitOnClick(event = None):
    global getName
    getName = nameData.get()
    getUID = uidData.get()
    loginErrorLabel = ttk.Label(root, font="mont", text="Sorry but it seems like\nyou aren't in the Voters' List!", justify=CENTER)
    adminSuccessLabel = ttk.Label(root, font="mont", text=f"Successfully logged in!\nWelcome {getName}!", justify=CENTER, padding=(70,0,70,0))
    loginErrorLabel.forget()
    adminSuccessLabel.forget()
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
        loginErrorLabel.destroy()
        adminSuccessLabel.grid(row=3, column=0, pady=(0,15), columnspan=2)
        try:
            adminWin.destroy()
        except NameError:
            pass
        openAdminWin()
    else:
        adminSuccessLabel.destroy()
        loginErrorLabel.grid(row=3, column=0, pady=(0,15), columnspan=2)
        try:
            adminWin.destroy()
        except NameError:
            pass


root.bind("<Return>", submitOnClick)

#main window widgets
nameLabel = ttk.Label(root, text="Enter your name:", font="mont").grid(row=0, column=0, padx=(100,10), pady=(100,10), sticky=W)
nameEntry = ttk.Entry(root, font="mont", textvariable=nameData).grid(row=0, column=1,padx=(10,100), pady=(100,10))
passLabel = ttk.Label(root, text="Enter your Password:", font="mont").grid(row=1, column=0, sticky=W, padx=(100,10), pady=(10,15))
passEntry = ttk.Entry(root, font="mont", textvariable=uidData, show="*").grid(row=1, column=1, padx=(10,100), pady=(10,15))
submitbtn = ttk.Button(root, text="Submit",command=submitOnClick, style="my.TButton").grid(row=2, column=0, pady=(5,100), columnspan=2)

openDebugWin()
root.mainloop()