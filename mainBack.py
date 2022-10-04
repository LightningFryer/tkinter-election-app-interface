# imports
import helper
import eAuth
import modify
import election

#--------------------------------------------------------Global Vars--------------------------------------------------------

voteCount = []

#--------------------------------------------------------Main Code--------------------------------------------------------
while True: #Main code starts here
    if helper.fetchAdminUsers() != []: #Check for existing admin user
        lg = eAuth.adminLogin()
        if lg[0]:
            while True:
                print("")
                print("1. Voters' List")
                print("2. Candidates' List")
                print("3. Admin Settings")
                print("4. Setup Voting Session")
                print("5. Start Voting Session")
                print("6. Logout")
                print("7. Close Program")

                try:
                    mainOp = input("Enter your choice: ")
                except:
                    print("Invalid Choice")
                    continue
                #Voters' List related operations
                if mainOp == "1":
                    while True:
                        subOp = election.subMenu() #Gets sub operation from this function
                        if subOp == "1": 
                            modify.voterAdd()

                        elif subOp == "2": 
                            modify.voterDelete()

                        elif subOp == "3": 
                            helper.displayVoters()
                        
                        elif subOp == "4":
                            print("Returning to main menu...")
                            break
                        else:
                            print("Invalid sub-operation!")

                #Candidates' List related operations
                elif mainOp == "2": 
                    while True:
                        subOp = election.subMenu() #Gets sub operation from this function
                        if subOp == "1": 
                            modify.candidateAdd()

                        elif subOp == "2":
                            modify.candidateDelete()
                        
                        elif subOp == "3":
                            helper.displayCandidates()
                            
                        elif subOp == "4":
                            print("Returning to main menu...")
                            break
                        else:
                            print("Invalid sub-operation!")
                
                #Admin related operations
                elif mainOp == "3": 
                    while True:
                        subOp = election.subMenuAdmin() #Gets sub operation for admin operations from this function
                        if subOp == "1": 
                            modify.adminCreate()
                        
                        elif subOp == "2":
                            modify.adminDelete()
                        
                        elif subOp == "3": 
                            helper.adminUpdate()

                        elif subOp == "4":
                            print("Returning to main menu...")
                            break
                        else:
                            print("Invalid sub-operation!")
                #Election settings
                elif mainOp == "4": 
                    allSettings = helper.fetchSettings() 
                    helper.displayAllSettings() #Displays settings of all sessions using PrettyTable
                    election.elecSettings(lg[1])
                
                #Election session
                elif mainOp == "5":
                    helper.displayAllSettings() #Displays settings of all sessions using PrettyTable
                    
                    sessionID = input("Session ID: ")
                    if helper.confirm():
                        settings = helper.fetchSettings(sessionID)
                        while True:
                            reply = election.elecSess(sessionID, settings, voteCount)
                            if reply[0]:
                                voteCount = reply[1]
                                continue
                            elif reply[2]:
                                continue
                            else:
                                election.saveSession(sessionID, voteCount)
                                print("Session saved...")
                                print("Exiting session")
                                break
                    else:
                        continue
                #Logout
                elif mainOp == "6":
                    break

                #Terminating instance
                elif mainOp == "7":
                    print("Terminating instance...")
                    print("Thank you for using Election App!")
                    exit()           
                
                else:
                    print("Invalid Operation!")
        else:
            print("Invalid Admin Details!")
    
    else:
        modify.adminCreate() #Prompt to create a new admin user if no pre-existing admin user is found
#^------------------------------------------------------^Main Code^------------------------------------------------------^
