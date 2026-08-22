#import the necessary modules
import random
import string

print("Moin, willkommen bei meinem personal Password Generator!")

#input password length
length = int(input("Wie viele Zeichen soll das Passwort haben? "))

#store different possible characters in a fitting variable / define data
buchstaben = string.ascii_letters
nummern = string.digits
zeichen = string.punctuation

#add data together
all = buchstaben + nummern + zeichen

#randomize the characters in the given length
temp = random.sample(all,length)

#create password by joining the characters
password = "".join(temp)

print(temp)