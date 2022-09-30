from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from urllib import response

from pyparsing import col
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
candData= StringVar()
voterNameData= StringVar()
voterAgeData= StringVar()
genderData= StringVar()
voterDelData= StringVar()
candNameData= StringVar()
candAgeData= StringVar()
candSymData= StringVar()
candDescData= StringVar()
candDelData = StringVar()
adminAddNameData = StringVar()
adminAddPassData = StringVar()
genderData.set(genders[0])

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
    voterListData = fetchVoters()
    
    fromVoterListBtn = ttk.Button(ListFrame, text="< Back", style="my.TButton", command=fromVoterList)
    fromVoterListBtn.grid(row=2, padx=(7,0), columnspan=2, pady=(15,0))
    voterListSep = ttk.Separator(ListFrame)
    voterListSep.grid(row=1, columnspan=2, sticky=EW, ipady=2)

    for i in range(1,len(voterListData)):
        if voterListData[i] != []:
            Label(canvasFrame, text=f"ID: {voterListData[i][0]}", font="mont").grid(row=i+1, column=0, sticky=W, padx=(180,100))
            Label(canvasFrame, text=f"Name: {voterListData[i][1]}", font="mont").grid(row=i+1, column=1, sticky=W)

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
        if candListData[i] != []:
            Label(canvasFrame, text=f"ID: {candListData[i][0]}   Name: {candListData[i][1]}   Age: {candListData[i][2]}   Sex: {candListData[i][3]}   Symbol: {candListData[i][4]}", font="mont").grid(row=i+1, column=0, sticky=W)

#Debug Window
def openDebugWin():
    global btnstyle
    global debugWin
    debugWin = Toplevel()
    debugWin.title("Debug Operations")
    consoleVoterListBtn = ttk.Button(debugWin, text="Voter List", command=fetchVotersDebug, style="my.TButton").grid(row=0, column=0, padx=15, ipadx=35, pady=15)
    consoleCandidateListBtn = ttk.Button(debugWin, text="Candidate List", command=fetchCandidatesDebug, style="my.TButton").grid(row=1, column=0, ipadx=30, pady=15)
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
        try:
            with open("Data/voterList.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow([UUIDgen, voterNameData.get(), voterAgeData.get(), genderData.get(), "N"])

            with open("Data/voterList.dat", "ab") as f:
                pickle.dump({"ID":UUIDgen, "Name":voterNameData.get()}, f)
            messagebox.showinfo(title="Success!", message="Successfully added details of Voter to Database!")
        except:
            messagebox.showerror(title="Error!", message="Unknown Excpetion! Could not add Voter Data to Database!")
    
def voterDelSubmit(event = None):
    found = False

    delVoterUUID = voterDelData.get()
    l = [] #Records to be rewritten are stored in this list

    data = fetchVoters()
    for i in data:
        if i != []:
            if i[0] == delVoterUUID: #Storing all records except the record to delete
                found = True
                continue
        l.append(i)
        
    if found:    
        messagebox.showinfo(title="Success!", message="Voter information successfully deleted!")
    else:
        messagebox.showerror(title="Error!", message=f"Sorry but we couldn't find the voter with ID {delVoterUUID} in the list!")

    with open("Data/voterList.csv", "w") as f: #Writing all the records except the record to delete
        writer = csv.writer(f)
        writer.writerows(l)

def candAddSubmit(event = None):
    addCandidateName = candNameData.get()
    addCandidateAge = candAgeData.get()
    addCandidateSex = genderData.get()
    addCandidateSymbol = candSymData.get()
    addCandidateDesc = candDescData.get()
    addCandidateID = str(uuid.uuid4()).split("-")[0]

    response = messagebox.askyesno(title="Confirmation", message=f"Are you sure you want to add details of {addCandidateName} to Database?")

    if response == 1:
        with open("Data/candidateList.csv", "a", encoding = 'utf8') as f:
            writer = csv.writer(f)
            writer.writerow([addCandidateID,addCandidateName,addCandidateAge,addCandidateSex,addCandidateSymbol,addCandidateDesc])
        messagebox.showinfo(title="Success!", message="Successfully added details of Candidate into Database!")

def candDelSubmit(event = None):
    delCandidateID = candDelData.get()
    found = False
    data = fetchCandidates()
    for i in data:
        if i != [] and i[0] == delCandidateID:
            found = True
            break
    if found:
        l = [] #Records to be rewritten are stored in this list
        for i in data:
            if i != [] and i[0] == delCandidateID: #Storing all the records except the one to be deleted
                continue
            l.append(i)

        with open("Data/candidateList.csv", 'w', encoding = 'utf8') as f: #Writing all the records except the one to be deleted
            writer = csv.writer(f)
            writer.writerows(l)
        messagebox.showinfo(title="Success!", message="Successfully deleted details of Candidate from Database!")
    else:
        messagebox.showerror(title="Error!", message="No such Candidate ID found in Database!")

def adminAddSubmit():
    adminName = adminAddNameData.get()
    adminPassword = adminAddPassData.get()
    cred = {"Admin Name":caesarCipher.caesarEncrypt(adminName), "Password":caesarCipher.caesarEncrypt(adminPassword)} #Dictionary containing new admin details to be dumped

    response = messagebox.askyesno(title="Confirmation", message="Are you sure you want to add details of new Admin to Database?")
    if response == 1:
        with open("Data/cred.dat", "ab") as f: #Dumping the new admin's data
            pickle.dump(cred, f)
        messagebox.showinfo(title="Success!", message="Successfully added details of Admin to Database!")

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

def openCandAddWin():
    hidePanel(candConfigFrame)
    showPanel(candAddFrame)

def openCandDelWin():
    hidePanel(candConfigFrame)
    showPanel(candDelFrame)

def openAdminAddWin():
    hidePanel(adminSettingsFrame)
    showPanel(adminAddFrame)

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

def fromCandAdd():
    hidePanel(candAddFrame)
    showPanel(candConfigFrame)

def fromCandDel():
    hidePanel(candDelFrame)
    showPanel(candConfigFrame)

def fromVoterDel():
    hidePanel(voterDelFrame)
    showPanel(voterConfigFrame)

def fromCandList():
    hidePanel(ListFrame)
    showPanel(candConfigFrame)

def fromAdminAdd():
    hidePanel(adminAddFrame)
    showPanel(adminSettingsFrame)

def adminLogout():
    hidePanel(adminFrame)
    showPanel(mainFrame)


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
addAdminProfile = ttk.Button(adminSettingsFrame, text="Create a new Admin Profile", style="my.TButton", command=openAdminAddWin)
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

#Admin Add Panel
adminAddFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
adminAddNameLabel = ttk.Label(adminAddFrame, text="Enter Admin Name:", font="mont")
adminAddNameEntry = ttk.Entry(adminAddFrame, textvariable=adminAddNameData, font="mont")
adminAddPassLabel = ttk.Label(adminAddFrame, text="Enter Admin Password:", font="mont")
adminAddPassEntry = ttk.Entry(adminAddFrame, textvariable=adminAddPassData, font="mont")
adminAddSubmitBtn = ttk.Button(adminAddFrame, text="Submit", style="my.TButton", command=adminAddSubmit)
fromAdminAddBtn = ttk.Button(adminAddFrame, text="< Back", style="my.TButton", command=fromAdminAdd)

adminAddNameLabel.grid(row=1, column=0, sticky=W)
adminAddNameEntry.grid(row=1, column=1)
adminAddPassLabel.grid(row=2, column=0, sticky=W)
adminAddPassEntry.grid(row=2, column=1)
adminAddSubmitBtn.grid(row=3, column=0, columnspan=2)
fromAdminAddBtn.grid(row=0, column=0, sticky=NW)

adminAddFrame.pack_forget()

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
addACandRecord = ttk.Button(candConfigFrame, text="Add a new Candidate record", style="my.TButton", command=openCandAddWin)
delACandRecord = ttk.Button(candConfigFrame, text="Delete a Candidate record", style="my.TButton", command=openCandDelWin)
displayCand = ttk.Button(candConfigFrame, text="Display Candidate List", style="my.TButton", command=showCandList)
fromCandConfigBtn = ttk.Button(candConfigFrame, text="< Back", style="my.TButton", command=fromCandConfig)

candConfigLabel.grid(row=1, column=0, columnspan=2, pady=(170,0), padx=(110,0))
candConfigLabelSep.grid(row=2, column=0, ipady=2, sticky=EW, columnspan=2, padx=(90,0), pady=(10,10))
addACandRecord.grid(row=3, column=0, padx=(90,5), ipadx=20, pady=(0,10))
delACandRecord.grid(row=3, column=1, padx=(5,0), ipadx=25, pady=(0,10))
displayCand.grid(row=4, column=0, columnspan=2, padx=(90,0), ipadx=25)
fromCandConfigBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

candConfigFrame.pack_forget()

#Candidate Add Panel
candAddFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
candNameAddLabel = ttk.Label(candAddFrame, text="Enter Candidate Name:", font="mont")
candNameAddEntry = ttk.Entry(candAddFrame, font="mont", textvariable=candNameData)
candAgeAddLabel = ttk.Label(candAddFrame, text="Enter Candidate Age:", font="mont")
candAgeAddEntry = ttk.Entry(candAddFrame, font="mont", textvariable=candAgeData)
candSymAddLabel = ttk.Label(candAddFrame, text="Enter Candidate Symbol:", font="mont")
candSymAddEntry = ttk.Entry(candAddFrame, font="mont", textvariable=candSymData)
candDescAddLabel = ttk.Label(candAddFrame, text="Enter Candidate Description:", font="mont")
candDescAddEntry = ttk.Entry(candAddFrame, font="mont", textvariable=candDescData)
candChooseGenderMenu = ttk.OptionMenu(candAddFrame, genderData, *genders, style="my.TOptionMenu")
candChooseGenderLabel = ttk.Label(candAddFrame, text="Choose Candidate Gender", font="mont")
candAddSubmitBtn = ttk.Button(candAddFrame, text="Submit", style="my.TButton", command=candAddSubmit)
fromCandAddBtn = ttk.Button(candAddFrame, text="< Back", style="my.TButton", command=fromCandAdd)

candNameAddLabel.grid(row=1, column=0, sticky=W, pady=(125,0), padx=(175,10))
candNameAddEntry.grid(row=1, column=1, pady=(125,10))
candAgeAddLabel.grid(row=2, column=0, sticky=W, padx=(175,10))
candAgeAddEntry.grid(row=2, column=1, pady=(0,10))
candSymAddLabel.grid(row=3, column=0, sticky=W, padx=(175,10))
candSymAddEntry.grid(row=3, column=1, pady=(0,10))
candDescAddLabel.grid(row=4, column=0, sticky=W, padx=(175,10))
candDescAddEntry.grid(row=4, column=1, pady=(0,10))
candChooseGenderLabel.grid(row=5, column=0, sticky=W, padx=(175,10))
candChooseGenderMenu.grid(row=5, column=1)
candAddSubmitBtn.grid(row=6, column=0, columnspan=2, padx=(175,0), pady=(15,0), ipadx=25)
fromCandAddBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

candAddFrame.pack_forget()

#Candidate Delete Panel

candDelFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
candDelLabel = ttk.Label(candDelFrame, text="Enter UID of Candidate:", font="mont")
candDelEntry = ttk.Entry(candDelFrame, textvariable=candDelData, font="mont")
candDelSubmitBtn = ttk.Button(candDelFrame, text="Submit", style="my.TButton", command=candDelSubmit)
fromCandDelBtn = ttk.Button(candDelFrame, text="< Back", style="my.TButton", command = fromCandDel)

candDelLabel.grid(row=1, column=0, sticky=W, padx=(200,10), pady=(175,0))
candDelEntry.grid(row=1, column=1, pady=(175,0))
candDelSubmitBtn.grid(row=2, column=0, columnspan=2, padx=(200,0), pady=(20,0), ipadx=20)
fromCandDelBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))


openDebugWin()
showPanel(mainFrame)
root.bind("<Return>", submitOnClick)
root.mainloop()
