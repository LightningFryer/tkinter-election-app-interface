import string

def caesarEncrypt(cipherText): #Encrypts the VOTER'S password
    lowerAlphabet = string.ascii_lowercase #returns a string of LOWERCASE alphabets into a varibale
    upperAlphabet = string.ascii_uppercase  #returns a string of UPPERCASE alphabets into a varibale
    
    shift = len(cipherText) #returns the length of the password into shift
    #print(shift) testing purposes
    encryptedText = '' #variable in which the new encrypted password will be stored

    for i in cipherText:
        if i.isalpha() and i.islower(): 
            pos = lowerAlphabet.index(i) #returns the index of the lowerAlphabet string with a letter from the password
            encryptedText += lowerAlphabet[(pos+shift)%26]
            #In case the password's letter's index exceeds the alphabet count 
            #(like the letter "z" for example), modulo operation with the length of the alphabet is done
        elif i.isalpha() and i.isupper(): #returns the index of the upperAlphabet string with a letter from the password
            pos = upperAlphabet.index(i)
            encryptedText += upperAlphabet[(pos+shift)%26]
        else: #for a "letter" that is either a number or a non-alphabet character
            encryptedText += i
    return encryptedText

def caesarDecrypt(cipherText): #decrypts the encrypted VOTER'S password
    lowerAlphabet = string.ascii_lowercase #Discussed above
    upperAlphabet = string.ascii_uppercase #Discussed above

    shift = len(cipherText) #returns length of the encrypted password into shift
    decryptedText = '' #variable in which the DECRPYTED password will be stored
    
    for i in cipherText:
        if i.isalpha() and i.islower():
            pos = lowerAlphabet.index(i)
            decryptedText += lowerAlphabet[(pos-shift)%26]
        elif i.isalpha() and i.isupper():
            pos = upperAlphabet.index(i)
            decryptedText += upperAlphabet[(pos-shift)%26]
        else:
            decryptedText += i
    return decryptedText

# print(caesarEncrypt('abcd123456789012345678901234567890'))
# print(caesarDecrypt(caesarEncrypt('abcd123456789012345678901234567890')))