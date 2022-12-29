from Key import *
from databaseSetup import *
from time import sleep

#first we need to run database setup
createDatabase()

# #print title/welcome message
print("Welcome to this dichotomous key program. In the following menu you will get options to create and run your own dichotomous keys. ")

#initilize response
response = 1

while response != 0:
    #print menu
    print("")
    print("Menu")
    print("1. Create a key")
    print("2. View keys")
    print("3. Run a key")
    print("4. Delete a key")
    # print("5. View species menu")
    print("0. Exit")
    print("")

    #get repsonse from user
    response = input("Type the number of your selection: ")
    print("")

    #do what the user requested
    if int(response) == 0:
        break

    elif int(response) == 1:
        enterKey()
    
    elif int(response) == 2:
        viewKeys()
    
    elif int(response) == 3:
        runKey(selectKey())
    
    elif int(response) == 4:
        key = selectKey()
        response = input("Are you sure you want to delete key? (Y/N) ")

        if response.upper() == "Y":
            deleteKey(key)
            print("Key deleted.")

    # elif int(response) == 5:
    #     pass

    else:
        print("Invalid reponse. Please select a menu item.")

#print closing message
print("Exit complete")

#wait a few seconds before exiting program
sleep(2)
