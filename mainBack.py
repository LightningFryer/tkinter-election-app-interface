# imports
from helper import *
from eAuth import *
from modify import *
from election import *

#--------------------------------------------------------Main Code--------------------------------------------------------

while True: #Main code starts here
    if fetchAdminUsers() != []:
        lg = adminLogin()
        if lg[0]:
            while True:
                print("1. Voters' List")
                print("2. Candidates' List")
                print("3. Admin Settings")
                print("4. Setup voting session")
                print("5. Start voting session")
                print("6. Logout")

                mainOp = int(input("Enter your choice: "))
                
                #Voters' List related operations
                if mainOp == 1:
                    while True:
                        subOp = subMenu() #Gets sub operation from this function
                        if subOp == 1: 
                            voterAdd()

                        elif subOp == 2: 
                            voterDelete()

                        elif subOp == 3: 
                            print(display_voters())
                        
                        elif subOp == 4:
                            print("Returning to main menu...")
                            break

                #Candidates' List related operations
                elif mainOp == 2: 
                    while True:
                        subOp = subMenu() #Gets sub operation from this function
                        if subOp == 1: 
                            candidateAdd()

                        elif subOp == 2:
                            candidateDelete()
                        
                        elif subOp == 3:
                            print(display_candidates())
                            
                        elif subOp == 4:
                            print("Returning to main menu...")
                            break
                
                #Admin related operations
                elif mainOp == 3: 
                    while True:
                        subOp = subMenuAdmin() #Gets sub operation for admin operations from this function
                        if subOp == 1: 
                            adminCreate()
                        
                        elif subOp == 2: 
                            adminDelete()
                        
                        elif subOp == 3: 
                            adminUpdate()

                        elif subOp == 4:
                            print("Returning to main menu...")
                            break
                
                #Election settings
                elif mainOp == 4: 
                    allSettings = fetchSettings() 
                    for i in allSettings: print(i) #lists settings of all sessions
                    elecSettings(lg[1])
                
                #Election session
                elif mainOp == 5:
                    confirmation = input("Are you sure?(y/n): ")
                    if confirmation.lower() == "y":
                        sessionID = input("Session ID: ")
                        settings = fetchSettings(sessionID)
                        while True:
                            elecSess(settings)
                            pass
                    else:
                        continue
                #Logout
                elif mainOp == 6:
                    break
                else:
                    print("Invalid Operation!")
        else:
            print("Invalid Admin Details!")
    
    else:
        adminCreate()
#^------------------------------------------------------^Main Code^------------------------------------------------------^
