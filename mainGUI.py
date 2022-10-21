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
adminNameData = StringVar()
adminPassData = StringVar()
adminNewPassData = StringVar()
elecPostData = StringVar()
boothNumData = StringVar()
startVoteSessIDData = StringVar()
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
    errorLabel = Label(canvasFrame, text="No Voter details found in database.\nYou can create new Voter Details from the previous menu.", font="mont", justify=CENTER)
    if voterListData == []:
        errorLabel.grid(row=0, column=0, padx=(90,0), pady=(250,0))
    else:
        errorLabel.grid_forget()
        voterIDLabel = ttk.Label(canvasFrame, text="ID", font="mont", justify=CENTER)
        voterNameLabel = ttk.Label(canvasFrame, text="Name", font="mont", justify=CENTER)
        voterAgeLabel = ttk.Label(canvasFrame, text="Age", font="mont", justify=CENTER)
        voterSexLabel = ttk.Label(canvasFrame, text="Sex", font="mont", justify=CENTER)
        voterVotedLabel = ttk.Label(canvasFrame,text="Voted?", font="mont", justify=CENTER)

        voterIDLabel.grid(row=0, column=0, padx=(150,10))
        voterNameLabel.grid(row=0, column=1, padx=(0,10))
        voterAgeLabel.grid(row=0, column=2, padx=(0,10))
        voterSexLabel.grid(row=0, column=3, padx=(0,10))
        voterVotedLabel.grid(row=0, column=4, padx=(0,10))

        for i in range(1,len(voterListData)):
            Label(canvasFrame, text=f"{voterListData[i][0]}", font="mont").grid(row=i+1, column=0, sticky=EW, padx=(150,10))
            Label(canvasFrame, text=f"{voterListData[i][1]}", font="mont").grid(row=i+1, column=1, sticky=EW, padx=(0,10))
            Label(canvasFrame, text=f"{voterListData[i][2]}", font="mont").grid(row=i+1, column=2, sticky=EW, padx=(0,10))
            Label(canvasFrame, text=f"{voterListData[i][3]}", font="mont").grid(row=i+1, column=3, sticky=EW, padx=(0,10))
            if voterListData[i][4] == "Y":
                Label(canvasFrame, text=f"Yes", font="mont").grid(row=i+1, column=4, sticky=EW)
            else:
                Label(canvasFrame, text=f"No", font="mont").grid(row=i+1, column=4, sticky=EW)

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
    errorLabel = Label(canvasFrame, text="No Candidate details found in database.\nYou can create new Candidate Details from the previous menu.", font="mont", justify=CENTER)
    if candListData == []:
        errorLabel.grid(row=0, column=0, padx=(90,0), pady=(250,0))
    else:
        errorLabel.grid_forget()
        candIDLabel = ttk.Label(canvasFrame, text="ID", font="mont", justify=CENTER)
        candNameLabel = ttk.Label(canvasFrame, text="Name", font="mont", justify=CENTER)
        candAgeLabel = ttk.Label(canvasFrame, text="Age", font="mont", justify=CENTER)
        candSexLabel = ttk.Label(canvasFrame, text="Sex", font="mont", justify=CENTER)
        candSymbolLabel = ttk.Label(canvasFrame,text="Symbol", font="mont", justify=CENTER)

        candIDLabel.grid(row=0, column=0, padx=(100,0))
        candNameLabel.grid(row=0, column=1)
        candAgeLabel.grid(row=0, column=2)
        candSexLabel.grid(row=0, column=3)
        candSymbolLabel.grid(row=0, column=4)
        for i in range(1,len(candListData)):
            Label(canvasFrame, text=f"{candListData[i][0]}", font="mont").grid(row=i+1, column=0, sticky=W, padx=(100,10))
            Label(canvasFrame, text=f"Name: {candListData[i][1]}", font="mont").grid(row=i+1, column=1, sticky=W, padx=(0,10))
            Label(canvasFrame, text=f"Age: {candListData[i][2]}", font="mont").grid(row=i+1, column=2, sticky=W, padx=(0,10))
            Label(canvasFrame, text=f"Sex: {candListData[i][3]}", font="mont").grid(row=i+1, column=3, sticky=W, padx=(0,10))
            Label(canvasFrame, text=f"Symbol: {candListData[i][4]}", font="mont").grid(row=i+1, column=4, sticky=W)

def showVoteSessList():
    hidePanel(setVoteSessFrame)
    global ListFrame, voteSessData
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
    voteSessData = fetchSettings()

    fromVoteSessListBtn = ttk.Button(ListFrame, text="< Back", style="my.TButton", command=fromVoteSessList)
    ListSep = ttk.Separator(ListFrame)
    fromVoteSessListBtn.grid(row=2, padx=(7,0), columnspan=2, pady=(15,0))
    ListSep.grid(row=1, columnspan=2, sticky=EW, ipady=2)
    errorLabel = Label(canvasFrame, text="No sessions exist as of now. Details of any sessions you create are shown here.\n Please create a session from the previous menu.", font="mont", justify=CENTER)

    if voteSessData == []:
        errorLabel.grid(row=0, column=0, padx=(90,0), pady=(250,0))
    else:
        errorLabel.grid_forget()
        sessIDHead = ttk.Label(canvasFrame, text="Session ID", font="mont")
        sessTimeHead = ttk.Label(canvasFrame, text="Time", font="mont")
        sessElecOffhead = ttk.Label(canvasFrame, text="Election Officer", font="mont")
        sessPostHead = ttk.Label(canvasFrame, text="Post", font="mont")
        sessBoothHead = ttk.Label(canvasFrame, text="Booth Number", font="mont")

        sessIDHead.grid(row=0, column=0, padx=(30,0), pady=(10,10))
        sessTimeHead.grid(row=0, column=1, padx=(30,0), pady=(10,10))
        sessElecOffhead.grid(row=0, column=2, padx=(30,0), pady=(10,10))
        sessPostHead.grid(row=0, column=3, padx=(30,0), pady=(10,10))
        sessBoothHead.grid(row=0, column=4, pady=(10,10), padx=(30,0))

        for i in range(len(voteSessData)):
            Label(canvasFrame, text=f"{voteSessData[i]['Session ID']}", font="mont").grid(row=i+1, column=0, padx=(30,0))
            Label(canvasFrame, text=f"{voteSessData[i]['Time']}", font="mont").grid(row=i+1, column=1, padx=(30,0))
            Label(canvasFrame, text=f"{voteSessData[i]['Election Officer']}", font="mont").grid(row=i+1, column=2, padx=(30,0))
            Label(canvasFrame, text=f"{voteSessData[i]['Post']}", font="mont").grid(row=i+1, column=3, padx=(30,0))
            Label(canvasFrame, text=f"{voteSessData[i]['Booth Number']}", font="mont").grid(row=i+1, column=4, padx=(15,0)) 

#Debug Window
def openDebugWin():
    global btnstyle
    global debugWin
    debugWin = Toplevel()
    debugWin.title("Debug Operations")
    consoleVoterListBtn = ttk.Button(debugWin, text="Voter List", command=fetchVoters, style="my.TButton").grid(row=0, column=0, padx=15, ipadx=35, pady=15)
    consoleCandidateListBtn = ttk.Button(debugWin, text="Candidate List", command=fetchCandidates, style="my.TButton").grid(row=1, column=0, ipadx=30, pady=15)
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

def adminAddSubmit(event = None):
    adminName = adminNameData.get()
    adminPassword = adminPassData.get()
    cred = {"Admin Name":caesarCipher.caesarEncrypt(adminName), "Password":caesarCipher.caesarEncrypt(adminPassword)} #Dictionary containing new admin details to be dumped

    response = messagebox.askyesno(title="Confirmation", message="Are you sure you want to add details of new Admin to Database?")
    if response == 1:
        with open("Data/cred.dat", "ab") as f: #Dumping the new admin's data
            pickle.dump(cred, f)
        messagebox.showinfo(title="Success!", message="Successfully added details of Admin to Database! You will now be sent back to login page to confirm this change.")
        hidePanel(adminAddFrame)
        showPanel(mainFrame)

def adminDelSubmit(event = None):
    adminName = adminNameData.get()
    adminPassword = adminPassData.get()
    f = open("Data/cred.dat", "rb")
    l = [] #Records to be rewritten are stored in this list
    found = False
    try: #Reading all records in cred.dat
        while True: #Storing all records except the one to be deleted
            data = pickle.load(f)
            if adminName != caesarCipher.caesarDecrypt(data['Admin Name']):
                l.append(data)
            elif adminName == caesarCipher.caesarDecrypt(data['Admin Name']):
                found = True
                if adminPassword != caesarCipher.caesarDecrypt(data["Password"]):
                    messagebox.showerror(title="Error!", message="Incorrect password of Admin given! Cannot authorise deletion of admin data without correct password so please try again!")
                    f.close() #Will close the file and no record would be modified/deleted
                    return
    except EOFError:
        f.close()
        if not found: #Checks if the inputted admin name exists in the first place or not 
            messagebox.showerror(title="Error!", message="Admin name does not exist in the database!") 
            return
        else:
            messagebox.showinfo(title="Success!", message="Successfully deleted information of Admin!")                
    with open("Data/cred.dat", "wb") as f: #Writing all records excluding the one to be deleted
        for i in l:
            pickle.dump(i, f)

def adminUpdateSubmit():
    adminUpdateErrorLabel.grid_forget()
    adminName = adminNameData.get()
    adminPassword = adminPassData.get()
    adminNewPassword = adminNewPassData.get()

    found = False
    f = open("Data/cred.dat", "rb")
    l = [] #Records to be rewritten are stored in this list
    try: #Searching for the record to be modified
        while True:
            data = pickle.load(f)
            if adminName == caesarCipher.caesarDecrypt(data['Admin Name']) and adminPassword == caesarCipher.caesarDecrypt(data["Password"]):
                found = True
            l.append(data)  
    except EOFError:
        f.close()
    if found: #Checks if the inputted admin name exists in the first place or not 
        response = messagebox.askyesno(title="Confirmation", message="Are you sure you want to change the password? This change is irrevocable if you forget the new password!")
        if response == 1:
            adminUpdateErrorLabel.grid_remove()
            for i in l:
                if caesarCipher.caesarDecrypt(i["Admin Name"]) ==  adminName:
                    i["Password"] = caesarCipher.caesarEncrypt(adminNewPassword) #Modifying the old password with the new password
            messagebox.showinfo(title="Success!", message=f"{adminName}'s password updated!")
    else:
        adminUpdateErrorLabel.grid(row=5, column=0, columnspan=2) 
    with open("Data/cred.dat", 'wb') as f: #Writing back all the records including the modified one
        for i in l:
            pickle.dump(i, f)

def setVoteSessSubmit(event = None):
    sessionID = str(uuid.uuid4()).split("-")[0]
    post = elecPostData.get()
    boothNo = boothNumData.get()
    response = messagebox.askyesno(title="Confirmation", message="Are you sure you want to create a new Voting Session?")
    
    if response == 1:
        voteCount = [["Candidate ID", "Candidate Name", "Votes"]]
        settingsFile = open("Data/settings.dat", "ab")
        timeStamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        settings = {"Session ID":sessionID, "Time": timeStamp, "Election Officer":nameData.get(), "Post":post, "Booth Number":boothNo}
        pickle.dump(settings,settingsFile)

        for i in helper.fetchCandidates()[1:]:
            voteCount.append([i[0],i[1],0])

        with open(f"Data/voteCount-{sessionID}.csv", "a", newline="") as voteCountFile:
            w_o = csv.writer(voteCountFile)
            w_o.writerows(voteCount)

        messagebox.showinfo(title="Success!", message="Successfully created new voting session!")

def startVoteSessSubmit(event = None):
    sessionID = startVoteSessIDData.get()
    found = False
    sessionData = fetchSettings()
    startVoteSessErrorLabel.grid_forget()
    for i in sessionData:
        if i["Session ID"] == sessionID:
            found = True
            break
    if found:
        startVoteSessErrorLabel.grid_forget()
        openVoteSessWin()
    else:
        startVoteSessErrorLabel.grid(row=3, column=0, columnspan=2)

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

def openAdminDelWin():
    hidePanel(adminSettingsFrame)
    showPanel(adminDelFrame)

def openAdminUpdateWin():
    hidePanel(adminSettingsFrame)
    showPanel(adminUpdateFrame)

def openSetVoteSessWin():
    hidePanel(adminFrame)
    showPanel(setVoteSessFrame)

def openStartVoteSessWin():
    hidePanel(adminFrame)
    showPanel(startVoteSessFrame)

def openVoteSessWin():
    hidePanel(startVoteSessFrame)
    showPanel(voteSessFrame)

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

def fromAdminDel():
    hidePanel(adminDelFrame)
    showPanel(adminSettingsFrame)

def fromAdminUpdate():
    hidePanel(adminUpdateFrame)
    showPanel(adminSettingsFrame)

def fromSetVoteSess():
    hidePanel(setVoteSessFrame)
    showPanel(adminFrame)

def fromVoteSessList():
    hidePanel(ListFrame)
    showPanel(setVoteSessFrame)

def fromStartVoteSess():
    hidePanel(startVoteSessFrame)
    showPanel(adminFrame)

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
loginErrorLabel = ttk.Label(mainFrame, font="mont", text="Sorry but it seems like\nyou aren't in the Admins' List!", justify=CENTER)

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
setVoteSessionBtn = ttk.Button(adminFrame, text="Setup Voting Session", style="my.TButton", command=openSetVoteSessWin)
startVoterSessionBtn = ttk.Button(adminFrame, text="Start a Voting Session", style="my.TButton", padding=(25,3,25,3), command=openStartVoteSessWin)
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
delAdminProfile = ttk.Button(adminSettingsFrame, text="Delete an Admin Profile   ", style="my.TButton", command=openAdminDelWin)
updateAdminProfile = ttk.Button(adminSettingsFrame, text="Update an Admin Profile", style="my.TButton", command=openAdminUpdateWin)
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
adminAddNameEntry = ttk.Entry(adminAddFrame, textvariable=adminNameData, font="mont")
adminAddPassLabel = ttk.Label(adminAddFrame, text="Enter Admin Password:", font="mont")
adminAddPassEntry = ttk.Entry(adminAddFrame, textvariable=adminPassData, font="mont")
adminAddSubmitBtn = ttk.Button(adminAddFrame, text="Submit", style="my.TButton", command=adminAddSubmit)
fromAdminAddBtn = ttk.Button(adminAddFrame, text="< Back", style="my.TButton", command=fromAdminAdd)

adminAddNameLabel.grid(row=1, column=0, sticky=W, pady=(170,10), padx=(200,10))
adminAddNameEntry.grid(row=1, column=1, pady=(170,10))
adminAddPassLabel.grid(row=2, column=0, sticky=W, padx=(200,10))
adminAddPassEntry.grid(row=2, column=1)
adminAddSubmitBtn.grid(row=3, column=0, columnspan=2, padx=(150,0), pady=(20,0), ipadx=25)
fromAdminAddBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

adminAddFrame.pack_forget()

#Admin Delete Panel
adminDelFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
adminDelNameLabel = ttk.Label(adminDelFrame, text="Enter Admin Name:", font="mont")
adminDelNameEntry = ttk.Entry(adminDelFrame, font="mont", textvariable=adminNameData)
adminDelPassLabel = ttk.Label(adminDelFrame, text="Enter Admin Password:", font="mont")
adminDelPassEntry = ttk.Entry(adminDelFrame, font="mont", textvariable=adminPassData)
adminDelSubmitBtn = ttk.Button(adminDelFrame, text="Submit", style="my.TButton", command=adminDelSubmit)
fromAdminDelBtn = ttk.Button(adminDelFrame, text="< Back", style="my.TButton", command=fromAdminDel)

adminDelNameLabel.grid(row=1, column=0, sticky=W, pady=(170,10), padx=(200,10))
adminDelNameEntry.grid(row=1, column=1, pady=(170,10))
adminDelPassLabel.grid(row=2, column=0, sticky=W, padx=(200,10))
adminDelPassEntry.grid(row=2, column=1)
adminDelSubmitBtn.grid(row=3, column=0, columnspan=2, padx=(150,0), pady=(20,0), ipadx=25)
fromAdminDelBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

adminDelFrame.pack_forget()

#Admin Update Panel
adminUpdateFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
adminUpdateNameLabel = ttk.Label(adminUpdateFrame, text="Enter Admin Name:", font="mont")
adminUpdateNameEntry = ttk.Entry(adminUpdateFrame, textvariable=adminNameData, font="mont")
adminUpdatePassLabel = ttk.Label(adminUpdateFrame, text="Enter Admin Password:", font="mont")
adminUpdatePassEntry = ttk.Entry(adminUpdateFrame, textvariable=adminPassData, font="mont", show="*")
adminUpdateNewPassLabel = ttk.Label(adminUpdateFrame, text="Enter New Password:", font="mont")
adminUpdateNewPassEntry = ttk.Entry(adminUpdateFrame, textvariable=adminNewPassData, font="mont", show="*")
adminUpdateSubmitBtn = ttk.Button(adminUpdateFrame, text="Submit", style="my.TButton", command=adminUpdateSubmit)
fromAdminUpdateBtn = ttk.Button(adminUpdateFrame, text="< Back", style="my.TButton", command=fromAdminUpdate)
adminUpdateErrorLabel = ttk.Label(adminUpdateFrame, text="Error! No such Admin Name exists\nwithin database!", justify=CENTER, font="mont")

adminUpdateNameLabel.grid(row=1, column=0, sticky=W, pady=(150,10), padx=(200,10))
adminUpdateNameEntry.grid(row=1, column=1, pady=(150,10))
adminUpdatePassLabel.grid(row=2, column=0, sticky=W, padx=(200,10))
adminUpdatePassEntry.grid(row=2, column=1, pady=(0,10))
adminUpdateNewPassLabel.grid(row=3, column=0, sticky=W, padx=(200,10))
adminUpdateNewPassEntry.grid(row=3, column=1)
adminUpdateSubmitBtn.grid(row=4, column=0, columnspan=2, padx=(150,0), pady=(20,10), ipadx=25)
fromAdminUpdateBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

adminUpdateFrame.pack_forget()

#Admin Voter Config Panel
voterConfigFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
voterConfigLabel = ttk.Label(voterConfigFrame, text="Voter Configuration", font="mont")
voterConfigLabelSep = ttk.Separator(voterConfigFrame)
addAVoterRecord = ttk.Button(voterConfigFrame, text="Add a new voter record", style="my.TButton", command=openVoterAddWin)
delAVoterRecord = ttk.Button(voterConfigFrame, text="Delete a voter record", style="my.TButton", command=openVoterDelWin)
displayVoters_ = ttk.Button(voterConfigFrame, text="Display Voter List", style="my.TButton", command=showVoterList)
fromVoterConfigBtn = ttk.Button(voterConfigFrame, text="< Back", style="my.TButton", command=fromVoterConfig)

voterConfigLabel.grid(row=1, column=0, columnspan=2, pady=(170,0), padx=(150,0))
voterConfigLabelSep.grid(row=2, column=0, ipady=2, sticky=EW, columnspan=2, padx=(130,0), pady=(10,10))
addAVoterRecord.grid(row=3, column=0, padx=(130,5), ipadx=20, pady=(0,10))
delAVoterRecord.grid(row=3, column=1, padx=(5,0), ipadx=25, pady=(0,10))
displayVoters_.grid(row=4, column=0, columnspan=2, padx=(100,0), ipadx=25)
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

voterDelFrame.pack_forget()

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
fromCandDelBtn = ttk.Button(candDelFrame, text="< Back", style="my.TButton", command=fromCandDel)

candDelLabel.grid(row=1, column=0, sticky=W, padx=(200,10), pady=(175,0))
candDelEntry.grid(row=1, column=1, pady=(175,0))
candDelSubmitBtn.grid(row=2, column=0, columnspan=2, padx=(200,0), pady=(20,0), ipadx=20)
fromCandDelBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

candDelFrame.pack_forget()

#Setup Voting Session Panel
setVoteSessFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
elecPostSessLabel = ttk.Label(setVoteSessFrame, text="Post of Election:", font="mont")
elecPostSessEntry = ttk.Entry(setVoteSessFrame, textvariable=elecPostData, font="mont")
boothNumLabel = ttk.Label(setVoteSessFrame, text="Enter Booth Number:", font="mont")
boothNumEntry = ttk.Entry(setVoteSessFrame, textvariable=boothNumData, font="mont")
setVoteSessSubmitBtn = ttk.Button(setVoteSessFrame, text="Submit", style="my.TButton", command=setVoteSessSubmit)
showVoteSessBtn = ttk.Button(setVoteSessFrame, text="Show Sessions", style="my.TButton", command=showVoteSessList)
fromSetVoteSessBtn = ttk.Button(setVoteSessFrame, text="< Back", style="my.TButton", command=fromSetVoteSess)

elecPostSessLabel.grid(row=1, column=0, sticky=W, padx=(200,10), pady=(175,10))
elecPostSessEntry.grid(row=1, column=1, pady=(175,10))
boothNumLabel.grid(row=2, column=0, sticky=W, padx=(200,10), pady=(0,20))
boothNumEntry.grid(row=2, column=1, pady=(0,20))
showVoteSessBtn.grid(row=3, column=0, padx=(200,10), sticky=EW, ipadx=30)
setVoteSessSubmitBtn.grid(row=3, column=1, sticky=EW)
fromSetVoteSessBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

setVoteSessFrame.pack_forget()

#Start Voting Session
startVoteSessFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)
startVoteSessIDLabel = ttk.Label(startVoteSessFrame, text="Enter Session ID:", font="mont")
startVoteSessIDEntry = ttk.Entry(startVoteSessFrame, textvariable=startVoteSessIDData, font="mont")
startVoteSessSubmitBtn = ttk.Button(startVoteSessFrame, text="Submit", style="my.TButton", command=startVoteSessSubmit)
fromStartVoteSessBtn = ttk.Button(startVoteSessFrame, text="< Back", style="my.TButton", command=fromStartVoteSess)
startVoteSessErrorLabel = ttk.Label(startVoteSessFrame, text="Sorry no such Session ID exists!", font="mont")

startVoteSessIDLabel.grid(row=1, column=0)
startVoteSessIDEntry.grid(row=1, column=1)
startVoteSessSubmitBtn.grid(row=2, column=0, columnspan=2)
fromStartVoteSessBtn.grid(row=0, column=0, sticky=NW, padx=(7,0), pady=(7,0))

startVoteSessFrame.pack_forget()

#Vote Session Frame
voteSessFrame = ttk.Frame(root, borderwidth=2, relief=SOLID)


if fetchAdminUsers() == []:
    fromAdminAddBtn.grid_forget()
    showPanel(adminAddFrame)
else:
    showPanel(mainFrame)

openDebugWin()
root.bind("<Return>", submitOnClick)
root.mainloop()
