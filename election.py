# imports
import datetime, pickle, uuid
from helper import *
from eAuth import *

#----------------------------------------------------------Menus----------------------------------------------------------

def subMenu(): #Displays a submenu for each main operation in the main program and returns the choice accordingly
    print("1. Add a record")
    print("2. Delete a record")
    print("3. Display records")
    print("4. Back")
    
    subOp = int(input("Enter your choice: "))   

    return subOp

def subMenuAdmin(): #Special sub menu for admin profile operations
    print("1. Create new admin profile")
    print("2. Delete an existing admin profile")
    print("3. Update an existing admin profile")
    print("4. Back")
    
    subOp = int(input("Enter your choice: "))
    
    return subOp

#^--------------------------------------------------------^Menus^--------------------------------------------------------^
#-----------------------------------------------------Election Session----------------------------------------------------

def elecSettings(admin):
    post = input("Post for which election is being conducted for: ")
    boothNo = input("Booth number: ")
    sessionID = str(uuid.uuid4()).split("-")[0]

    confirmation = input("Confirm settings?(y/n): ")
    if confirmation.lower() == "y":
        settingsFile = open("settings.dat", "ab")
        timeStamp = datetime.datetime.now()
        settings = {"Session ID":sessionID, "Time": timeStamp, "Election Officer":admin,"Post":post,"Booth Number":boothNo}
        pickle.dump(settings,settingsFile)
        return settings
    else: 
        print("Aborting...")
        return

def elecSess(settings):
    if voterLogin():
        print("Candidate List:")
        print(display_candidates())
        print("")
        post = settings["Post"]
        print(f"Aforementioned table is the list of candidates for the election standing for {post}.\nYou may pick the candidate of your choice by submitting the unique id associated with the candidate (see candidate list — first column)")
        
        data = fetchCandidates()
        # need to add code to loop after voter login if voter wishes to recast vote
        while True:
            ch = input("Your choice: ")
            for i in data:
                if ch == i[0]:
                    print(f"You have chosen to vote for {i[1]}")
                    # confirming vote
                    confirmation = input("Are you sure?(y/n): ")
                    if confirmation.lower() == "y":
                        # need to store records of vote count for each candidate in a file
                        print("Vote casted successfully!")
                        return True
                    else:
                        print("Recast your vote!")
                        continue
    else:
        print("Incorrect voter credentials!")

#^---------------------------------------------------^Election Session^--------------------------------------------------^