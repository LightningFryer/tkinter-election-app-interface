# imports
import pickle, caesarCipher, csv
import election
#---------------------------------------------------------Logins----------------------------------------------------------

def adminLogin(): #Admin login details check
    print("")
    print("Log in as administrator")
    adminName = input("Admin Name: ")
    adminPassword = input("Password: ")
    f = open("Data/cred.dat", "rb")
    try:
        while True:
            data = pickle.load(f)
            if adminName == caesarCipher.caesarDecrypt(data['Admin Name']) and adminPassword == caesarCipher.caesarDecrypt(data["Password"]):
                f.close() 
                return (True,adminName)
    except EOFError:
        f.close() 
        return (False,)


def voterLogin(): #Checks whether the VOTER'S name and UID exists within the database and correspond to each other
    print("")
    print("Log in as voter")
    ID = input("ID: ")
    name = input("Name: ")
    
    if ID == "EXIT" or name == "EXIT":
        return "EXIT"
        
    f = open("Data/voterList.csv", 'r', newline="")
    reader = csv.reader(f)
    
    for i in reader:
        if ID == i[0] and name == i[1] and election.hasVoted(ID) == False:
            f.close()
            return True
    f.close()
    return False

#^-------------------------------------------------------^Logins^--------------------------------------------------------^
