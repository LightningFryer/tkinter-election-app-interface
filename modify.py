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

        with open("Election App/Data/cred.dat", "ab") as f: #Dumping the new admin's data
            pickle.dump(cred, f) 
        print(f"Added {adminName} as an administrator!")
    else:
        print("Aborting...")

def adminDelete(): #Allows the admin to delete an existing admin profile
    print("Submit the credentials of the admin user to be removed...")
    adminName = input("Enter Admin Name: ")
    adminPassword = input("Enter admin password: ")
    
    if confirm():
        f = open("Election App/Data/cred.dat", "rb")
        l = [] #Records to be rewritten are stored in this list

        try: #Reading all records in cred.dat
            while True: #Storing all records except the one to be deleted
                data = pickle.load(f)
                if adminName != caesarCipher.caesarDecrypt(data['Admin Name']):
                    l.append(data)
                elif adminName == caesarCipher.caesarDecrypt(data['Admin Name']):
                    if adminPassword != caesarCipher.caesarDecrypt(data["Password"]):
                        print("Incorrect password!\nAdmin user cannot be terminated without authorisation")
                        f.close()
                        return
        except EOFError:
            f.close()

        with open("Election App/Data/cred.dat", "wb") as f: #Writing all records excluding the one to be deleted
            for i in l:
                pickle.dump(i, f)
    else:
        print("Aborting...")

def adminUpdate(): #Allows the admin to update an existing admin profile
    adminName = input("Admin Name: ")
    adminPassword = input("Password: ")
    
    if confirm():
        f = open("Election App/Data/cred.dat", "rb")
        l = [] #Records to be rewritten are stored in this list

        try: #Searching for the record to be modified
            while True:
                data = pickle.load(f)
                if adminName == caesarCipher.caesarDecrypt(data['Admin Name']) and adminPassword == caesarCipher.caesarDecrypt(data["Password"]):
                    adminNewPassword = input("New password: ")
                    data["Password"] = adminNewPassword #Modifying the old password with the new password
                    print("Updated password!")
                else:
                    print("Incorrect admin name or password!")
                    f.close()
                    return
                l.append(data)  
        except EOFError:
            f.close()

        with open("Election App/Data/cred.dat", 'wb') as f: #Writing back all the records including the modified one
            for i in l:
                pickle.dump(i, f)
        print(f"{adminName}'s password updated!")
    else:
        print("Aborting...")

# Modifying voters' list
def voterAdd(): #To add a record to voterList.csv and update voterList.dat with a new UUID accordingly
    addVoterName = input("Enter voter name to add to list: ")
    addVoterAge = input(f"Enter {addVoterName}'s age: ")
    addVoterSex = input(f"Enter {addVoterName}'s gender: ")
    addVoterUUID = str(uuid.uuid4()).split("-")[0]

    if confirm():
        with open("Election App/Data/voterList.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([addVoterName,addVoterAge,addVoterSex])

        with open("Election App/Data/voterList.dat", "ab") as f:
            pickle.dump({"ID":addVoterUUID, "Name":addVoterName}, f)

        print(f"Successfully added {addVoterName}'s details into the voters' list")
    else:
        print("Aborting")

def voterDelete(): #To delete a record from voterList.csv and voterList.dat
    delVoterID = input("Enter voter's ID to delete from list: ")

    if confirm():
        l = [] #Records to be rewritten are stored in this list

        data = fetchVotersBIN() 
        for i in data:
            if data["ID"] == delVoterID: #Storing all the records except the record to delete
                print(f"Successfully deleted {delVoterID}'s details from the records")
                delVoterName = data["Name"]
                continue
            l.append(i)

        with open("Election App/Data/voterList.dat", 'wb') as f: #Writing all the records except the record to delete
            for i in l:
                pickle.dump(i, f)

        l = [] #Records to be rewritten are stored in this list

        data = fetchVotersCSV()
        for i in data:
            if i[0] != delVoterName: #Storing all records except the record to delete
                l.append(i)

        with open("Election App/Data/voterList.csv", "w") as f: #Writing all the records except the record to delete
            writer = csv.writer(f)
            writer.writerows(l)
    else:
        print("Aborting...")

# Modifying candidates' list
def candidateAdd(): #Adds details of a NEW CANDIDATE into candidateList.csv
    addCandidateName = input("Enter voter name to add to list: ")
    addCandidateAge = input(f"Enter {addCandidateName}'s age: ")
    addCandidateSex = input(f"Enter {addCandidateName}'s gender: ")
    addCandidateAbout = input(f"Enter {addCandidateName}'s description: ")
    addCandidateID = str(uuid.uuid4()).split("-")[0]
    
    if confirm():
        with open("Election App/Data/candidateList.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([addCandidateID,addCandidateName,addCandidateAge,addCandidateSex,addCandidateAbout])
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

        with open("Election App/Data/candidateList.csv", 'w') as f: #Writing all the records except the one to be deleted
            writer = csv.writer(f)
            writer.writerows(l)
    else:
        print("Aborting...")

#^--------------------------------------------------^Modifying records^--------------------------------------------------^