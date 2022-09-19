from tkinter import *
from tkinter import ttk
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
    hidePanel(mainFrame)
    showPanel(adminFrame)

def showVoterList():
    hidePanel(voterConfigFrame)
    global voterListFrame
    voterListFrame = ttk.Frame(root)
    voterListFrame.grid(row=0, column=0, sticky=NSEW, ipadx=200)
    voterListFrame.grid_rowconfigure(0, weight=1)
    voterListFrame.grid_columnconfigure(0, weight=1)

    voterListCanvas = Canvas(voterListFrame)
    voterListCanvas.grid(row=0, column=0, sticky=NSEW+W, ipady=130)
    voterListCanvas.grid_rowconfigure(0, weight=1)
    voterListCanvas.grid_columnconfigure(0, weight=1)

    scroll = ttk.Scrollbar(voterListFrame, orient=VERTICAL, command= voterListCanvas.yview)
    scroll.grid(sticky=NS+E, column=1, row=0)

    voterListCanvas.configure(yscrollcommand=scroll.set)
    voterListCanvas.bind("<Configure>", lambda e: voterListCanvas.configure(scrollregion=voterListCanvas.bbox("all")))

    canvasFrame = ttk.Frame(voterListCanvas)
    voterListCanvas.create_window((0,0), window=canvasFrame, anchor=NW)
    global voterListData
    voterListData = fetchVotersBIN()
    fromVoterListBtn = ttk.Button(voterListFrame, text="< Back", style="my.TButton", command=fromVoterList)
    fromVoterListBtn.grid(row=1, padx=(7,0), columnspan=2, pady=(15,0))
    
    for i in range(len(voterListData)):
        Label(canvasFrame, text=f"ID: {voterListData[i]['ID']}", font="mont").grid(row=i+1, column=0, sticky=W, padx=(180,100))
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
        loginErrorLabel.grid(row=3, column=0, columnspan=2, padx=(95,0), pady=(30,0))

def showPanel(frameName):
    frameName.pack(fill=BOTH, expand=True, padx=10, pady=10)

def hidePanel(frameName):
    frameName.pack_forget()

def openAdminSettings():
    hidePanel(adminFrame)
    showPanel(adminSettingsFrame)

def openVoterConfig():
    hidePanel(adminFrame)
    showPanel(voterConfigFrame)

def goBack():
    hidePanel(adminSettingsFrame)
    openAdminWin()

def fromVoterConfig():
    hidePanel(voterConfigFrame)
    openAdminWin()

def fromVoterList():
    hidePanel(voterListFrame)
    showPanel(voterConfigFrame)

def adminLogout():
    hidePanel(adminFrame)
    showPanel(mainFrame)

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
mainFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
nameLabel = ttk.Label(mainFrame, text="Enter your name:", font="mont")
nameEntry = ttk.Entry(mainFrame, font="mont", textvariable=nameData)
passLabel = ttk.Label(mainFrame, text="Enter your Password:", font="mont")
passEntry = ttk.Entry(mainFrame, font="mont", textvariable=uidData, show="*")
loginbtn = ttk.Button(mainFrame, text="Login",command=submitOnClick, style="my.TButton")
loginErrorLabel = ttk.Label(mainFrame, font="mont", text="Sorry but it seems like\nyou aren't in the Voters' List!", justify=CENTER)

nameLabel.grid(row=0, column=0, sticky=W, padx=(200,30), pady=(220,0))
nameEntry.grid(row=0, column=1, padx=(15,90), pady=(220,0))
passLabel.grid(row=1, column=0, sticky=W, padx=(200,0), pady=(20,0))
passEntry.grid(row=1, column=1, padx=(15,90), pady=(20,0))
loginbtn.grid(row=2, column=0, columnspan=2, pady=(30,0), padx=(100,0), ipadx=40)

mainFrame.pack_forget()

#admin Main Window
adminFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
adminWinLabel = ttk.Label(adminFrame, text="Welcome Admin", font="mont")
adminLabelSep = ttk.Separator(adminFrame)
voterOpBtn = ttk.Button(adminFrame, text="Configure Voters' List", style="my.TButton", command=openVoterConfig)
candidateOpBtn = ttk.Button(adminFrame, text="Configure Candidates' List", style="my.TButton")
setVoteSessionBtn = ttk.Button(adminFrame, text="Setup Voting Session", style="my.TButton")
startVoterSessionBtn = ttk.Button(adminFrame, text="Start a Voting Session", style="my.TButton", padding=(25,3,25,3))
adminSettingBtn = ttk.Button(adminFrame, text="Admin Settings", style="my.TButton", command=openAdminSettings)
adminLogoutBtn = ttk.Button(adminFrame, text="Logout", style="my.TButton", padding=(20,3,20,3), command=adminLogout)

adminWinLabel.grid(row=0, column=0, columnspan=2, pady=(170,5), padx=(150,0))
adminLabelSep.grid(row=1, column=0, columnspan=2, padx=(145,0), ipady=2, sticky=EW)
voterOpBtn.grid(row=2, column=0, padx=(150,5), pady=(10,10), ipadx=15)
candidateOpBtn.grid(row=2, column=1, padx=(10,5), pady=(10,10))
setVoteSessionBtn.grid(row=3, column=0, padx=(150,5), pady=(10,10), ipadx=15)
startVoterSessionBtn.grid(row=3, column=1, padx=(10,5), pady=(10,10))
adminSettingBtn.grid(row=4, column=0, padx=(130,0), pady=(10,10), columnspan=2)
adminLogoutBtn.grid(row=5, column=0, padx=(130,0), pady=(10,10), columnspan=2)

adminFrame.pack_forget()

#admin Settings Window
adminSettingsFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
adminSetttingLabel = ttk.Label(adminSettingsFrame, text="Admin Settings", font="mont")
adminSetttingLabelSep = ttk.Separator(adminSettingsFrame)
addAdminProfile = ttk.Button(adminSettingsFrame, text="Create a new Admin Profile", style="my.TButton")
delAdminProfile = ttk.Button(adminSettingsFrame, text="Delete an Admin Profile   ", style="my.TButton")
updateAdminProfile = ttk.Button(adminSettingsFrame, text="Update an Admin Profile", style="my.TButton")
backButton = ttk.Button(adminSettingsFrame, text="< Back", style="my.TButton", command=goBack)

adminSetttingLabel.grid(row=1, column=0, columnspan=2, pady=(150,15), padx=(150,0))
adminSetttingLabelSep.grid(row=2, column=0, columnspan=2, padx=(150,0), pady=(0,10), ipady=2, sticky=EW)
addAdminProfile.grid(row=3, column=0, padx=(150,5))
delAdminProfile.grid(row=3, column=1, padx=(5,0), ipadx=10)
updateAdminProfile.grid(row=4, column=0, columnspan=2, padx=(125,0), pady=(15,0))
backButton.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

adminSettingsFrame.pack_forget()

#Admin Voter Config Panel
voterConfigFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
addAVoterRecord = ttk.Button(voterConfigFrame, text="Add a new voter record", style="my.TButton")
delAVoterRecord = ttk.Button(voterConfigFrame, text="Delete a voter record", style="my.TButton")
displayVoters = ttk.Button(voterConfigFrame, text="Display Voter List", style="my.TButton", command=showVoterList)
fromVoterConfigBtn = ttk.Button(voterConfigFrame, text="< Back", style="my.TButton", command=fromVoterConfig)

addAVoterRecord.grid(row=1, column=0, padx=(150,5), pady=(200,15), ipadx=20)
delAVoterRecord.grid(row=1, column=1, padx=(5,60), pady=(200,15), ipadx=25)
displayVoters.grid(row=2, column=0, columnspan=2, padx=(100,0), ipadx=25)
fromVoterConfigBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

voterConfigFrame.pack_forget()

openDebugWin()
showPanel(mainFrame)
root.bind("<Return>", submitOnClick)
root.mainloop()
