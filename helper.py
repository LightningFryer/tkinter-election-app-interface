# imports
import pickle, csv
from prettytable import PrettyTable

#----------------------------------------------------------Misc-----------------------------------------------------------

def elecPrompt(): #Prompt to accept name and UID of VOTERS
    name = input("Name: ")
    UID = input("UID: ")
    return name, UID

def confirm(): #Prompt to confirm user choice
    confirmation = input("Are you sure?(y/n): ")
    if confirmation.lower() == "y":
        return True
    else:
        return False
#^--------------------------------------------------------^Misc^---------------------------------------------------------^
#----------------------------------------------------Fetching records-----------------------------------------------------

def fetchCandidates():
    data = []
    with open("Data/candidateList.csv", 'r', encoding = 'utf8', newline="") as f:
        reader = csv.reader(f)
        for i in reader:
            data.append(i)
    return data

def fetchVoters():
    data = []
    with open("Data/voterList.csv", 'r', newline="") as f:
        reader = csv.reader(f)
        for i in reader:
            data.append(i)
    return data
    
def fetchSettings(sessionID=None):
    if sessionID is None:
        settingsFile = open("Data/settings.dat", "rb")
        settingsList = []
        try:
            while True:
                settings = pickle.load(settingsFile)
                settingsList.append(settings)
        except EOFError:
            settingsFile.close()
        return settingsList
    else:
        settingsFile = open("Data/settings.dat", "rb")
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
    credFile = open("Data/cred.dat", "rb")
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

def displayCandidates(): #Displays the candidates details for the voters to see using prettytable  
    candidateData = fetchCandidates()
    
    candidateTable = PrettyTable(candidateData[0]) #Creates a table with headers from the csv file.
    
    for row in candidateData[1:]:
        candidateTable.add_row([row[0],row[1],row[2],row[3],row[4],row[5]]) #Adds rows into candidateTable one by one
    
    print(candidateTable)

def displayVoters(): #Displays the voter details for the admin to see using prettytable  
    voterData = fetchVoters()

    voterTable = PrettyTable(voterData[0]) #Creates a table with headers from the csv file. 
    
    for row in voterData[1:]:
        voterTable.add_row([row[0],row[1],row[2],row[3],row[4]]) #Adds rows into voterTable one by one
    
    print(voterTable)
#^-------------------------------------------------^Displaying records^--------------------------------------------------^    
