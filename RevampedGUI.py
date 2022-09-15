from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import SimpleDialog
from helper import *
from eAuth import *
from modify import *
from election import *
import sv_ttk as theme

#main window
root = Tk()
root.title("Election App Mockup")
theme.set_theme("dark")
root.geometry("800x600")
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
    L = [nameLabel, nameEntry, passLabel, passEntry, loginbtn, loginErrorLabel]
    hideWidgetsOnScreen(L)
    adminWinLabel.grid(row=0, column=0, columnspan=2, pady=(170,5), padx=(150,0))
    voterOpBtn.grid(row=1, column=0, padx=(150,5), pady=(10,10), ipadx=15)
    candidateOpBtn.grid(row=1, column=1, padx=(10,5), pady=(10,10))
    setVoteSessionBtn.grid(row=2, column=0, padx=(150,5), pady=(10,10), ipadx=15)
    startVoterSessionBtn.grid(row=2, column=1, padx=(10,5), pady=(10,10))
    adminSettingBtn.grid(row=3, column=0, padx=(130,0), pady=(10,10), columnspan=2)
    adminLogoutBtn.grid(row=4, column=0, padx=(130,0), pady=(10,10), columnspan=2)

def showVoterList():
    hideWidgetsOnScreen([nameLabel, nameEntry, passLabel, passEntry, loginbtn, loginErrorLabel])
    voterListFrame = ttk.Frame(root)
    voterListFrame.pack(fill=BOTH, expand=1, padx=(200,0))
    voterListCanvas = Canvas(voterListFrame)
    voterListCanvas.pack(side=LEFT, fill=BOTH, expand=1)
    scroll = ttk.Scrollbar(voterListFrame, orient=VERTICAL, command = voterListCanvas.yview)
    scroll.pack(side=RIGHT, fill=Y)

    voterListCanvas.configure(yscrollcommand=scroll.set)
    voterListCanvas.bind("<Configure>", lambda e: voterListCanvas.configure(scrollregion=voterListCanvas.bbox("all")))

    canvasFrame = ttk.Frame(voterListCanvas)
    voterListCanvas.create_window((0,0), window=canvasFrame, anchor=NW)
    voterListData = fetchVotersBIN()

    backButton.pack(padx=(7,0), pady=(0,7), anchor=NW, side=TOP)
    
    for i in range(len(voterListData)):
        Label(canvasFrame, text=f"ID: {voterListData[i]['ID']},{' '*10}", font="mont").grid(row=i+1, column=0, sticky=W)
        Label(canvasFrame, text=f"Name: {voterListData[i]['Name']}", font="mont").grid(row=i+1, column=1, sticky=W)

def openDebugWin():
    global btnstyle
    global debugWin
    debugWin = Toplevel()
    debugWin.title("Debug Operations")
    consoleVoterListBtn = ttk.Button(debugWin, text="Voter List", command=showVoterList, style="my.TButton").grid(row=0, column=0, padx=15, ipadx=35, pady=15)
    consoleCandidateListBtn = ttk.Button(debugWin, text="Candidate List", command=display_candidates_debug, style="my.TButton").grid(row=1, column=0, ipadx=30, pady=15)
    autoLogin = ttk.Button(debugWin, text="Admin Login", command=openAdminWin, style="my.TButton").grid(row=2, column=0, padx=15, pady=15, ipadx=35,)
    testList = ttk.Button(debugWin, text="Test List", command=showVoterList, style="my.TButton").grid(row=3, column=0, padx=15, pady=15)

# def testScroll():
#     hideWidgetsOnScreen([nameLabel, nameEntry, passLabel, passEntry, loginbtn, loginErrorLabel])
#     voterListFrame = ttk.Frame(root)
#     voterListFrame.pack(fill=BOTH, expand=1, pady=(0,100))
#     voterListCanvas = Canvas(voterListFrame)
#     voterListCanvas.pack(side=LEFT, fill=BOTH, expand=1)
#     scroll = ttk.Scrollbar(voterListFrame, orient=VERTICAL, command = voterListCanvas.yview)
#     scroll.pack(side=RIGHT, fill=Y)

#     voterListCanvas.configure(yscrollcommand=scroll.set)
#     voterListCanvas.bind("<Configure>", lambda e: voterListCanvas.configure(scrollregion=voterListCanvas.bbox("all")))

#     canvasFrame = ttk.Frame(voterListCanvas)
#     voterListCanvas.create_window((0,0), window=canvasFrame, anchor=NW)
    
#     for i in range(1,51):
#         Label(canvasFrame, text=f"Line {i}. Sample Text for padding purposes", font="mont").pack()


def submitOnClick(event = None):
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
        loginErrorLabel.grid()


root.bind("<Return>", submitOnClick)

def showMainWidgets():
    nameLabel.grid(row=0, column=0, sticky=W, padx=(200,30), pady=(220,0))
    nameEntry.grid(row=0, column=1, padx=(15,90), pady=(220,0))
    passLabel.grid(row=1, column=0, sticky=W, padx=(200,0), pady=(20,0))
    passEntry.grid(row=1, column=1, padx=(15,90), pady=(20,0))
    loginbtn.grid(row=2, column=0, columnspan=2, pady=(30,0), padx=(100,0), ipadx=40)

def openAdminSettings():
    L = [adminWinLabel, voterOpBtn, candidateOpBtn, setVoteSessionBtn, startVoterSessionBtn, adminSettingBtn, adminLogoutBtn]
    hideWidgetsOnScreen(L)
    addAdminProfile.grid(row=1, column=0, padx=(150,5), pady=(200,15))
    delAdminProfile.grid(row=1, column=1, padx=(5,60), pady=(200,15))
    updateAdminProfile.grid(row=2, column=0, columnspan=2, padx=(100,0))
    backButton.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

def goBack():
    addAdminProfile.grid_remove()
    delAdminProfile.grid_remove()
    updateAdminProfile.grid_remove()
    backButton.grid_remove()
    openAdminWin()

def hideWidgetsOnScreen(listOfWidgets):
    for i in listOfWidgets:
        i.grid_forget()

def showWidgetsOnScreen(listOfWidgets):
    for i in listOfWidgets:
        i.grid()

def adminLogout():
    hide = [adminWinLabel, voterOpBtn, candidateOpBtn, setVoteSessionBtn, startVoterSessionBtn, adminSettingBtn, adminLogoutBtn]
    hideWidgetsOnScreen(hide)
    showMainWidgets()

# def adminCreate(): #Allows the admin to add a new admin user
#     adminName = input("Admin Name: ")
#     adminPassword = input("Password: ")
#     if confirm():
#         cred = {"Admin Name":caesarCipher.caesarEncrypt(adminName), "Password":caesarCipher.caesarEncrypt(adminPassword)} #Dictionary containing new admin details to be dumped

#         with open("Data/cred.dat", "ab") as f: #Dumping the new admin's data
#             pickle.dump(cred, f) 
#         print(f"Added {adminName} as an administrator!")
#     else:
#         print("Aborting...")

#main window widgets
nameLabel = ttk.Label(root, text="Enter your name:", font="mont")
nameEntry = ttk.Entry(root, font="mont", textvariable=nameData)
passLabel = ttk.Label(root, text="Enter your Password:", font="mont")
passEntry = ttk.Entry(root, font="mont", textvariable=uidData, show="*")
loginbtn = ttk.Button(root, text="Login",command=submitOnClick, style="my.TButton")
loginErrorLabel = ttk.Label(root, font="mont", text="Sorry but it seems like\nyou aren't in the Voters' List!", justify=CENTER)

#admin Window
addAdminProfile = ttk.Button(root, text="Create a new Admin Profile", style="my.TButton")
delAdminProfile = ttk.Button(root, text="Delete an Admin Profile   ", style="my.TButton")
updateAdminProfile = ttk.Button(root, text="Update an Admin Profile", style="my.TButton")

backButton = ttk.Button(root, text="< Back", style="my.TButton", command=goBack)

#admin Settings
adminWinLabel = ttk.Label(root, text="Welcome Admin", font="mont")
voterOpBtn = ttk.Button(root, text="Configure Voters' List", style="my.TButton")
candidateOpBtn = ttk.Button(root, text="Configure Candidates' List", style="my.TButton")
setVoteSessionBtn = ttk.Button(root, text="Setup Voting Session", style="my.TButton")
startVoterSessionBtn = ttk.Button(root, text="Start a Voting Session", style="my.TButton", padding=(25,3,25,3))
adminSettingBtn = ttk.Button(root, text="Admin Settings", style="my.TButton", command=openAdminSettings)
adminLogoutBtn = ttk.Button(root, text="Logout", style="my.TButton", padding=(20,3,20,3), command=adminLogout)

openDebugWin()
showMainWidgets()
root.mainloop()
