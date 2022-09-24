from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from helper import *
from eAuth import *
from modify import *
from election import *
import sv_ttk as theme

#main window
root = Tk()
root.title("Election App Mockup")
theme.set_theme("dark")
winWidth, winHeight = 800, 600
screenWidth, screenHeight = root.winfo_screenwidth(), root.winfo_screenheight()
x = (screenWidth/2) - (winWidth/2)
y = (screenHeight/2) - (winHeight/2)
root.geometry(f"{winWidth}x{winHeight}+{int(x)}+{int(y)}")
root.resizable(0,0)

crntPanel = ""

#btn style
btnstyle = ttk.Style().configure("my.TButton", font=("mont",))
#radiobtn style
radioStyle = ttk.Style().configure("my.TRadiobutton", font=("mont",))
#Label fram style
framestyle = ttk.Style().configure("my.TLabelframe", font=("mont",))
#Option Menu Style
opmenustyle = ttk.Style().configure("my.TOptionMenu", font=("mont",))

#textvariable data of buttons/OptionMenu is stored here        
genders = ["Male", "Male", "Female", "Other"]
nameData = StringVar()
uidData = StringVar()
candData = StringVar()
voterNameData = StringVar()
voterAgeData = StringVar()
genderData = StringVar()
genderData.set(genders[0])
voterDelData = StringVar()

#Voter/Candidate Lists 
def showVoterList():
    hidePanel(voterConfigFrame)
    global ListFrame, voterListData
    ListFrame = ttk.Frame(root)
    ListFrame.grid(row=0, column=0, sticky=NSEW, ipadx=200)
    ListFrame.grid_rowconfigure(0, weight=1)
    ListFrame.grid_columnconfigure(0, weight=1)

    ListCanvas = Canvas(ListFrame)
    ListCanvas.grid(row=0, column=0, sticky=NSEW+W, ipady=130)
    ListCanvas.grid_rowconfigure(0, weight=1)
    ListCanvas.grid_columnconfigure(0, weight=1)

    scroll = ttk.Scrollbar(ListFrame, orient=VERTICAL, command= ListCanvas.yview)
    scroll.grid(sticky=NS+E, column=1, row=0)

    ListCanvas.configure(yscrollcommand=scroll.set)
    ListCanvas.bind("<Configure>", lambda e: ListCanvas.configure(scrollregion=ListCanvas.bbox("all")))

    canvasFrame = ttk.Frame(ListCanvas)
    ListCanvas.create_window((0,0), window=canvasFrame, anchor=NW)
    voterListData = fetchVotersBIN()
    
    fromVoterListBtn = ttk.Button(ListFrame, text="< Back", style="my.TButton", command=fromVoterList)
    fromVoterListBtn.grid(row=2, padx=(7,0), columnspan=2, pady=(15,0))
    voterListSep = ttk.Separator(ListFrame)
    voterListSep.grid(row=1, columnspan=2, sticky=EW, ipady=2)

    for i in range(len(voterListData)):
        Label(canvasFrame, text=f"ID: {voterListData[i]['ID']}", font="mont").grid(row=i+1, column=0, sticky=W, padx=(180,100))
        Label(canvasFrame, text=f"Name: {voterListData[i]['Name']}", font="mont").grid(row=i+1, column=1, sticky=W)

def showCandList():
    hidePanel(candConfigFrame)
    global ListFrame, candListData
    ListFrame = ttk.Frame(root)
    ListFrame.grid(row=0, column=0, sticky=NSEW, ipadx=200)
    ListFrame.grid_rowconfigure(0, weight=1)
    ListFrame.grid_columnconfigure(0, weight=1)

    ListCanvas = Canvas(ListFrame)
    ListCanvas.grid(row=0, column=0, sticky=NSEW+W, ipady=130)
    ListCanvas.grid_rowconfigure(0, weight=1)
    ListCanvas.grid_columnconfigure(0, weight=1)

    scroll = ttk.Scrollbar(ListFrame, orient=VERTICAL, command= ListCanvas.yview)
    scroll.grid(sticky=NS+E, column=1, row=0)

    ListCanvas.configure(yscrollcommand=scroll.set)
    ListCanvas.bind("<Configure>", lambda e: ListCanvas.configure(scrollregion=ListCanvas.bbox("all")))

    canvasFrame = ttk.Frame(ListCanvas)
    ListCanvas.create_window((0,0), window=canvasFrame, anchor=NW)
    candListData = fetchCandidates()

    fromCandListBtn = ttk.Button(ListFrame, text="< Back", style="my.TButton", command=fromCandList)
    candListSep = ttk.Separator(ListFrame)
    fromCandListBtn.grid(row=2, padx=(7,0), columnspan=2, pady=(15,0))
    candListSep.grid(row=1, columnspan=2, sticky=EW, ipady=2)

    for i in range(1,len(candListData)):
        Label(canvasFrame, text=f"ID: {candListData[i][0]}   Name: {candListData[i][1]}   Age: {candListData[i][2]}   Sex: {candListData[i][3]}   Symbol: {candListData[i][4]}", font="mont").grid(row=i+1, column=0, sticky=W)

#Debug Window
def openDebugWin():
    global btnstyle
    global debugWin
    debugWin = Toplevel()
    debugWin.title("Debug Operations")
    consoleVoterListBtn = ttk.Button(debugWin, text="Voter List", command=display_voters_debug, style="my.TButton").grid(row=0, column=0, padx=15, ipadx=35, pady=15)
    consoleCandidateListBtn = ttk.Button(debugWin, text="Candidate List", command=display_candidates_debug, style="my.TButton").grid(row=1, column=0, ipadx=30, pady=15)
    autoLogin = ttk.Button(debugWin, text="Admin Login", command=openAdminWin, style="my.TButton").grid(row=2, column=0, padx=15, pady=15, ipadx=35,)
    testList = ttk.Button(debugWin, text="Test List", command=showVoterList, style="my.TButton").grid(row=3, column=0, padx=15, pady=15)

#Submit Button Commands
def submitOnClick(event = None):
    loginErrorLabel.grid_remove()
    adminListDAT = open("Data/cred.dat", "rb")
    found = 0
    try:
        while True:
            dataAdmin = pickle.load(adminListDAT)
            if nameData.get() == caesarCipher.caesarDecrypt(dataAdmin["Admin Name"]) and uidData.get() == caesarCipher.caesarDecrypt(dataAdmin["Password"]):
                found = 1
                break
    except EOFError:
        adminListDAT.close()
    if found == 1:
        loginErrorLabel.grid_remove()
        openAdminWin()
    else:
        loginErrorLabel.grid(row=3, column=0, columnspan=2, padx=(95,0), pady=(30,0))

def voterAddSubmit(event = None):
    UUIDgen = str(uuid.uuid4()).split("-")[0]
    response = messagebox.askyesno(title="Are you sure?", message="Do you want to add Voter's details to Databse?")
    if response == 1:
        with open("Data/voterList.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([voterNameData.get(), voterAgeData.get(), int(genderData.get())])

        with open("Data/voterList.dat", "ab") as f:
            pickle.dump({"ID":UUIDgen, "Name":voterNameData.get()}, f)
        messagebox.showinfo(title="Success!", message="Successfully added details of Voter to Database!")
    
def voterDelSubmit(event = None):
    l = [] #Records to be rewritten are stored in this list
    delVoterID = voterDelData.get()
    response = messagebox.askyesno(title="Are you sure?", message=f"Are you sure you want to delete Voter {delVoterID}'s data?")
    found = 0
    if response == 1:
        data = fetchVotersBIN() 
        for i in data:
            if data["ID"] == delVoterID:
                found = 1
                break
        if found == 1:
            messagebox.showinfo("Successfully deleted Voter information!")
            for i in data:
                if data["ID"] == delVoterID: #Storing all the records except the record to delete
                    delVoterName = data["Name"]
                    continue
                l.append(i)

            with open("Data/voterList.dat", 'wb') as f: #Writing all the records except the record to delete
                for i in l:
                    pickle.dump(i, f)

            l = [] #Records to be rewritten are stored in this list

            data = fetchVotersCSV()
            for i in data:
                if i[0] != delVoterName: #Storing all records except the record to delete
                    l.append(i)

            with open("Data/voterList.csv", "w") as f: #Writing all the records except the record to delete
                writer = csv.writer(f)
                writer.writerows(l)
        else:
            messagebox.showerror(title="Voter Not Found!", message=f"Sorry but we couldn't find the voter with ID {delVoterID} in the list!")

#Show/Hide Panel Commands
def showPanel(frameName):
    frameName.pack(fill=BOTH, expand=True, padx=10, pady=10)

def hidePanel(frameName):
    try:
        frameName.pack_forget()
        frameName.grid_forget()
    except:
        pass

#Open Window Commands
def openAdminWin():
    hidePanel(mainFrame)
    showPanel(adminFrame)
    crntPanel = "adminWin"

def openCandWin():
    hidePanel(adminFrame)
    showPanel(candConfigFrame)

def openAdminSettingsWin():
    crntPanel = "adminSettings"
    hidePanel(adminFrame)
    showPanel(adminSettingsFrame)

def openVoterConfigWin():
    crntPanel = "voterConfig"
    hidePanel(adminFrame)
    showPanel(voterConfigFrame)

def openVoterAddWin():
    hidePanel(voterConfigFrame)
    showPanel(voterAddFrame)

def openVoterDelWin():
    hidePanel(voterConfigFrame)
    showPanel(voterDelFrame)

#Close/Hide Windows
def fromAdminSettings():
    hidePanel(adminSettingsFrame)
    openAdminWin()

def fromVoterConfig():
    hidePanel(voterConfigFrame)
    openAdminWin()

def fromCandConfig():
    hidePanel(candConfigFrame)
    openAdminWin()

def fromVoterList():
    hidePanel(ListFrame)
    showPanel(voterConfigFrame)

def fromAddVoter():
    hidePanel(voterAddFrame)
    showPanel(voterConfigFrame)

def fromVoterDel():
    hidePanel(voterDelFrame)
    showPanel(voterConfigFrame)

def fromCandList():
    hidePanel(ListFrame)
    showPanel(candConfigFrame)

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
nameEntry = ttk.Entry(mainFrame, font="mont",textvariable=nameData)
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
voterOpBtn = ttk.Button(adminFrame, text="Configure Voters' List", style="my.TButton", command=openVoterConfigWin)
candidateOpBtn = ttk.Button(adminFrame, text="Configure Candidates' List", style="my.TButton", command=openCandWin)
setVoteSessionBtn = ttk.Button(adminFrame, text="Setup Voting Session", style="my.TButton")
startVoterSessionBtn = ttk.Button(adminFrame, text="Start a Voting Session", style="my.TButton", padding=(25,3,25,3))
adminSettingBtn = ttk.Button(adminFrame, text="Admin Settings", style="my.TButton", command=openAdminSettingsWin)
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
backButton = ttk.Button(adminSettingsFrame, text="< Back", style="my.TButton", command=fromAdminSettings)

adminSetttingLabel.grid(row=1, column=0, columnspan=2, pady=(150,15), padx=(150,0))
adminSetttingLabelSep.grid(row=2, column=0, columnspan=2, padx=(150,0), pady=(0,10), ipady=2, sticky=EW)
addAdminProfile.grid(row=3, column=0, padx=(150,5))
delAdminProfile.grid(row=3, column=1, padx=(5,0), ipadx=10)
updateAdminProfile.grid(row=4, column=0, columnspan=2, padx=(125,0), pady=(15,0))
backButton.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

adminSettingsFrame.pack_forget()

#Admin Voter Config Panel
voterConfigFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
voterConfigLabel = ttk.Label(voterConfigFrame, text="Voter Configuration", font="mont")
voterConfigLabelSep = ttk.Separator(voterConfigFrame)
addAVoterRecord = ttk.Button(voterConfigFrame, text="Add a new voter record", style="my.TButton", command=openVoterAddWin)
delAVoterRecord = ttk.Button(voterConfigFrame, text="Delete a voter record", style="my.TButton", command=openVoterDelWin)
displayVoters = ttk.Button(voterConfigFrame, text="Display Voter List", style="my.TButton", command=showVoterList)
fromVoterConfigBtn = ttk.Button(voterConfigFrame, text="< Back", style="my.TButton", command=fromVoterConfig)

voterConfigLabel.grid(row=1, column=0, columnspan=2, pady=(170,0), padx=(150,0))
voterConfigLabelSep.grid(row=2, column=0, ipady=2, sticky=EW, columnspan=2, padx=(130,0), pady=(10,10))
addAVoterRecord.grid(row=3, column=0, padx=(130,5), ipadx=20, pady=(0,10))
delAVoterRecord.grid(row=3, column=1, padx=(5,0), ipadx=25, pady=(0,10))
displayVoters.grid(row=4, column=0, columnspan=2, padx=(100,0), ipadx=25)
fromVoterConfigBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

voterConfigFrame.pack_forget()

#Add Voter Win
voterAddFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
voterNameAddLabel = ttk.Label(voterAddFrame, text="Enter voter Name:", font="mont")
voterAgeAddLabel = ttk.Label(voterAddFrame, text="Enter voter Age:", font="mont")
voterAgeAddEntry = ttk.Entry(voterAddFrame, font="mont", textvariable=voterAgeData)
voterAgeAddEntry.insert(0,"")
voterNameAddEntry = ttk.Entry(voterAddFrame, font="mont", textvariable=voterNameData)
voterChooseGenderMenu = ttk.OptionMenu(voterAddFrame, genderData, *genders, style="my.TOptionMenu")
voterChooseGenderLabel = ttk.Label(voterAddFrame, text="Choose Voter Gender", font="mont")
voterAddSubmitBtn = ttk.Button(voterAddFrame, text="Submit", style="my.TButton", command=voterAddSubmit)
fromAddVoterBtn = ttk.Button(voterAddFrame, text="< Back", style="my.TButton", command=fromAddVoter)

fromAddVoterBtn.grid(row=0, column=0, padx=(7,0), pady=(7,0), sticky=NW)
voterNameAddLabel.grid(row=1, column=0, sticky=W, padx=(175,0), pady=(175,10))
voterNameAddEntry.grid(row=1, column=1, pady=(175,10))
voterAgeAddLabel.grid(row=2, column=0, sticky=W, padx=(175,10))
voterAgeAddEntry.grid(row=2, column=1, pady=(0,20))
voterChooseGenderLabel.grid(row=3, column=0, sticky=W, padx=(175,0))
voterChooseGenderMenu.grid(row=3, column=1)
voterAddSubmitBtn.grid(row=4, column=0, columnspan=2, padx=(175,0), pady=(20,0), ipadx=15)

voterAddFrame.pack_forget()

#Delete a Voter Frame
voterDelFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
voterDelLabel = ttk.Label(voterDelFrame, text="Enter UID of Voter:", font="mont")
voterDelEntry = ttk.Entry(voterDelFrame, textvariable=voterDelData, font="mont")
voterDelSubmitBtn = ttk.Button(voterDelFrame, text="Submit", style="my.TButton", command=voterDelSubmit)
fromVoterDelBtn = ttk.Button(voterDelFrame, text="< Back", style="my.TButton", command = fromVoterDel)

voterDelLabel.grid(row=1, column=0, sticky=W, padx=(200,10), pady=(175,0))
voterDelEntry.grid(row=1, column=1, pady=(175,0))
voterDelSubmitBtn.grid(row=2, column=0, columnspan=2, padx=(200,0), pady=(20,0), ipadx=20)
fromVoterDelBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

#Admin Candidate Config Panel
candConfigFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
candConfigLabel = ttk.Label(candConfigFrame, text="Candidate Configuration", font="mont")
candConfigLabelSep = ttk.Separator(candConfigFrame)
addACandRecord = ttk.Button(candConfigFrame, text="Add a new Candidate record", style="my.TButton")
delACandRecord = ttk.Button(candConfigFrame, text="Delete a Candidate record", style="my.TButton")
displayCand = ttk.Button(candConfigFrame, text="Display Candidate List", style="my.TButton", command=showCandList)
fromCandConfigBtn = ttk.Button(candConfigFrame, text="< Back", style="my.TButton", command=fromCandConfig)

candConfigLabel.grid(row=1, column=0, columnspan=2, pady=(170,0), padx=(110,0))
candConfigLabelSep.grid(row=2, column=0, ipady=2, sticky=EW, columnspan=2, padx=(90,0), pady=(10,10))
addACandRecord.grid(row=3, column=0, padx=(90,5), ipadx=20, pady=(0,10))
delACandRecord.grid(row=3, column=1, padx=(5,0), ipadx=25, pady=(0,10))
displayCand.grid(row=4, column=0, columnspan=2, padx=(90,0), ipadx=25)
fromCandConfigBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

candConfigFrame.pack_forget()

openDebugWin()
showPanel(mainFrame)
root.bind("<Return>", submitOnClick)
root.mainloop()
