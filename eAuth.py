# imports
import pickle, caesarCipher

#---------------------------------------------------------Logins----------------------------------------------------------

def adminLogin(): #Admin login details check
    adminName = input("Admin Name: ")
    adminPassword = input("Password: ")
    f = open("cred.dat", "rb")
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
    name = input("Name: ")
    ID = input("ID: ")
    votersFile = open("voterList.dat", "rb")
    try:
        while True:
            voterData = pickle.load(votersFile)
            if voterData["Name"] == name and voterData["ID"] == ID:
                votersFile.close()
                return True
    except EOFError:
        votersFile.close() 
        return False

#^-------------------------------------------------------^Logins^--------------------------------------------------------^
