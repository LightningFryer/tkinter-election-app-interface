# imports
import datetime, pickle, uuid, csv
import helper
import eAuth

#----------------------------------------------------------Menus----------------------------------------------------------

def subMenu(): #Displays a submenu for each main operation in the main program and returns the choice accordingly
    print("")
    print("1. Add a record")
    print("2. Delete a record")
    print("3. Display records")
    print("4. Back")

    subOp = input("Enter your choice: ")

    return subOp

def subMenuAdmin(): #Special sub menu for admin profile operations
    print("")
    print("1. Create new admin profile")
    print("2. Delete an existing admin profile")
    print("3. Update an existing admin profile")
    print("4. Back")

    subOp = input("Enter your choice: ")
    
    return subOp

#^--------------------------------------------------------^Menus^--------------------------------------------------------^
#-----------------------------------------------------Election Session----------------------------------------------------


def elecSettings(admin):
    post = input("Post for which election is being conducted for: ")
    boothNo = input("Booth number: ")
    sessionID = str(uuid.uuid4()).split("-")[0]
    
    if helper.confirm():
        voteCount = [["Candidate ID", "Candidate Name", "Votes"]]
        settingsFile = open("Data/settings.dat", "ab")
        timeStamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        settings = {"Session ID":sessionID, "Time": timeStamp, "Election Officer":admin, "Post":post, "Booth Number":boothNo}
        pickle.dump(settings,settingsFile)
        
        for i in helper.fetchCandidates()[1:]:
            voteCount.append([i[0],i[1],0])
        
        with open(f"Data/voteCount-{sessionID}.csv", "a", newline="") as voteCountFile:
            w_o = csv.writer(voteCountFile)
            w_o.writerows(voteCount)

        return voteCount
    else: 
        print("Aborting...")
        return

def elecSess(sessionID, settings,voteCount): #Starts a election session using an existing session id (check a file named voteCount-SessionID.csv)
    if voteCount == []:
        with open(f"Data/voteCount-{sessionID}.csv", "r", newline="") as voteCountFile:
            r_o = csv.reader(voteCountFile)
            for i in r_o: voteCount.append(i)

    if eAuth.voterLogin(): #Login check for voter
        print("Candidate List:")
        helper.displayCandidates()
        print("") #Prints an empty line after the candidate list is printed
        post = settings["Post"] #Settings recieved from main from input
        print(f"Aforementioned table is the list of candidates for the election standing for {post}.\nYou may pick the candidate of your choice by submitting the unique id associated with the candidate (see candidate list ??? first column)")
        
        data = helper.fetchCandidates() #Gets candidate data from candidateList.csv

        while True:
            ch = input("Your choice: ")
            if ch == "EXIT":
                print("Saving session...")
                return (False, voteCount, False) #(Has voted - False, voteCount List, Exit loop) 
            
            for i in data[1:]: #Ignoring heading of csv file and iterating through rest
                if ch == i[0]:
                    print(f"You have chosen to vote for {i[1]}")
                    # confirming vote
                    if helper.confirm():
                        voteCount = vote(i[0], voteCount) #Accepts the candidate id and votecount and increments voteCount by 1
                        print("Vote casted successfully!")
                        # print(voteCount)
                        return (True, voteCount, False) #(Has voted - True, voteCount List, Exit loop)
                    else:
                        print("Recast your vote!")
                        pass
            else:
                print("Candidate ID does not exist! Check the candidate list's ID column carefully and vote again")
    else:
        print("Incorrect voter credentials!")
        return(False, voteCount, True) #(Has voted - False, voteCount List, Continue loop) 

def vote(choiceID, voteCount):
    for i in voteCount:
        if choiceID == i[0]:
            voteCount[voteCount.index(i)][2] = 1+int(voteCount[voteCount.index(i)][2])
            return voteCount

def saveSession(sessionID, voteCount):
    with open(f"Data/voteCount-{sessionID}.csv", "w", newline="") as voteCountFile:
            w_o = csv.writer(voteCountFile)
            w_o.writerows(voteCount)

def hasVoted(ID):
    voterData = helper.fetchVoters()
    for i in voterData[1:]:
        if i[0] == ID and i[4] == "Y":
            return True
    return False
#^---------------------------------------------------^Election Session^--------------------------------------------------^
