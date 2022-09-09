# imports
import pickle, csv
from prettytable import PrettyTable

def elecPrompt(): #Prompt to accept name and UID of VOTERS
    name = input("Name: ")
    UID = input("UID: ")
    return name, UID

def confirm():
    confirmation = input("Are you sure?(y/n): ")
    if confirmation.lower() == "y":
        return True
    else:
        return False

#----------------------------------------------------Fetching records-----------------------------------------------------

def fetchCandidates():
    data = []
    with open("Data/candidateList.csv", 'r', encoding = 'utf8') as f:
        reader = csv.reader(f)
        for i in reader:
            data.append(i)
    return data

def fetchVotersCSV():
    data = []
    with open("Election App/Data/voterList.csv", 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            data.append(i)
    return data

def fetchVotersBIN():
    data = []
    f = open("Data/voterList.dat", 'rb')
    try:
        while True:
            i = pickle.load(f)
            data.append(i)
    except EOFError:
        f.close()
    return data

def fetchSettings(sessionID=None):
    if sessionID is None:
        settingsFile = open("Election App/Data/settings.dat", "rb")
        settingsList = []
        try:
            while True:
                settings = pickle.load(settingsFile)
                settingsList.append(settings)
        except EOFError:
            settingsFile.close()
        return settingsList
    else:
        settingsFile = open("Election App/Data/settings.dat", "rb")
        try:
            while True:
                settings = pickle.load(settingsFile)
                if settings["Session ID"] == sessionID:
                    print("Session found!")
                    return settings
        except EOFError:
            print("No such session exists!")
            settingsFile.close()

def fetchAdminUsers():
    credFile = open("Election App/Data/cred.dat", "rb")
    adminUsers = []
    try:
        while True:
            adminUser = pickle.load(credFile)
            adminUsers.append(adminUser)
    except EOFError:
        credFile.close()
    return adminUsers

#^--------------------------------------------------^Fetching records^---------------------------------------------------^
#---------------------------------------------------Displaying records----------------------------------------------------

def display_candidates_debug():
    data = fetchCandidates()
    for i in data: print(i)

def display_candidates(): #Displays the candidates details for the voters to see using prettytable  
    candidateTable = PrettyTable(["ID","Name","Age","Sex","Symbol","About"]) #Creates a table with headers from the csv file.
    
    candidateData = fetchCandidates()
    
    for row in candidateData:
        if row[4] != "Symbol": 
            candidateTable.add_row([row[0],row[1],row[2],row[3],row[4],row[5]]) #Adds rows into candidateTable one by one
    
    return candidateTable

def display_voters_debug(): #Displays the voter details for the admin to see using prettytable  
    data = fetchVotersBIN()
    for i in data: print(i)

    # Need to modify pretty table code to make use of data from binary file 
    # voterTable = PrettyTable(["Name","Age","Sex"]) #Creates a table with headers from the csv file. 

    # voterData = fetchVotersCSV()
    
    # for row in voterData:
    #     if row[1] != "Age": 
    #         voterTable.add_row([row[0],row[1],row[2]]) #Adds rows into voterTable one by one
    
    # return voterTable

#^-------------------------------------------------^Displaying records^--------------------------------------------------^