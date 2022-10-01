# imports
from helper import *
import caesarCipher, pickle, csv, uuid

#----------------------------------------------------Modifying records----------------------------------------------------

# Modifying admin user details
def adminCreate(): #Allows the admin to add a new admin user
    adminName = input("Admin Name: ")
    adminPassword = input("Password: ")
    if confirm():
        cred = {"Admin Name":caesarCipher.caesarEncrypt(adminName), "Password":caesarCipher.caesarEncrypt(adminPassword)} #Dictionary containing new admin details to be dumped

        with open("Data/cred.dat", "ab") as f: #Dumping the new admin's data
            pickle.dump(cred, f) 
        print(f"Added {adminName} as an administrator!")
    else:
        print("Aborting...")

def adminDelete(): #Allows the admin to delete an existing admin profile
    print("Submit the credentials of the admin user to be removed...")
    adminName = input("Enter Admin Name: ")
    adminPassword = input("Enter Admin Password: ")
    
    if confirm():
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
                        print("Incorrect password!\nAdmin user cannot be terminated without authorisation")
                        f.close() #Will close the file and no record would be modified/deleted
                        return
        except EOFError:
            f.close()
            if not found: #Checks if the inputted admin name exists in the first place or not 
                print("Admin name does not exist in the database!") 
                return                

        with open("Data/cred.dat", "wb") as f: #Writing all records excluding the one to be deleted
            for i in l:
                pickle.dump(i, f)
    else:
        print("Aborting...")

def adminUpdate(): #Allows the admin to update an existing admin profile
    adminName = input("Admin Name: ")
    adminPassword = input("Password: ")
    found = False
    if confirm():
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
            adminNewPassword = input("New password: ")
            for i in l:
                if caesarCipher.caesarDecrypt(i["Admin Name"]) ==  adminName:
                    i["Password"] = caesarCipher.caesarEncrypt(adminNewPassword) #Modifying the old password with the new password
            print(f"{adminName}'s password updated!")
        else:
            print("Admin name does not exist in the database!") 
            return

        with open("Data/cred.dat", 'wb') as f: #Writing back all the records including the modified one
            for i in l:
                pickle.dump(i, f)
        print(l)
    else:
        print("Aborting...")

# Modifying voters' list
def voterAdd(): #To add a record to voterList.csv and update voterList.dat with a new UUID accordingly
    addVoterName = input("Enter voter name to add to list: ")
    addVoterAge = input(f"Enter {addVoterName}'s age: ")
    addVoterSex = input(f"Enter {addVoterName}'s gender: ")
    addVoterUUID = str(uuid.uuid4()).split("-")[0]

    if confirm():
        with open("Data/voterList.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([addVoterUUID,addVoterName,addVoterAge,addVoterSex,'N'])

        print(f"Successfully added {addVoterName}'s details into the voters' database!")
    else:
        print("Aborting")

def voterDelete(): #To delete a record from voterList.csv and voterList.dat
    found = False

    delVoterUUID = input("Enter voter's UUID to delete from the database: ")

    if confirm():

        l = [] #Records to be rewritten are stored in this list

        data = fetchVoters()
        for i in data:
            if i[0] == delVoterUUID: #Storing all records except the record to delete
                found = True
                print("Deleted {delVoterUUID}'s details from the database!")
                continue
            l.append(i)
        
        if not found:
            print("No such voter exists in the database!")
            return

        with open("Data/voterList.csv", "w") as f: #Writing all the records except the record to delete
            writer = csv.writer(f)
            writer.writerows(l)
    else:
        print("Aborting...")

# Modifying candidates' list
def candidateAdd(): #Adds details of a NEW CANDIDATE into candidateList.csv
    addCandidateName = input("Enter candidate name to add to list: ")
    addCandidateAge = input(f"Enter {addCandidateName}'s age: ")
    addCandidateSex = input(f"Enter {addCandidateName}'s gender: ")
    addCandidateSymbol = input(f"Enter {addCandidateName}'s symbol: ")
    addCandidateAbout = input(f"Enter {addCandidateName}'s description: ")
    addCandidateID = str(uuid.uuid4()).split("-")[0]
    
    if confirm():
        with open("Data/candidateList.csv", "a", encoding = 'utf8') as f:
            writer = csv.writer(f)
            writer.writerow([addCandidateID,addCandidateName,addCandidateAge,addCandidateSex,addCandidateSymbol,addCandidateAbout])
        print(f"Successfully added {addCandidateName}'s details into the records")
    else:
        print("Aborting...")

def candidateDelete(): #Deletes details of an existing CANDIDATE from candidateList.csv
    delCandidateID = input("Enter the Candidate's ID to be deleted: ")

    if confirm():
        l = [] #Records to be rewritten are stored in this list

        data = fetchCandidates() 
        for i in data:
            if i[0] == delCandidateID: #Storing all the records except the one to be deleted
                print(f"Successfully deleted details of Candidate with ID {delCandidateID}")
                continue
            l.append(i)

        with open("Data/candidateList.csv", 'w', encoding = 'utf8') as f: #Writing all the records except the one to be deleted
            writer = csv.writer(f)
            writer.writerows(l)
    else:
        print("Aborting...")

#^--------------------------------------------------^Modifying records^--------------------------------------------------^
