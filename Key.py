import sqlite3
import Nodes
import Functions 

#TODO sqllite cursors or connections? Idk enough about thenm
#TODO add logging to everything in this file
#TODO I kind of want to get rid of the Functions file and jsut do everything in here?

#funtion to enter a new dichotmous key into the database
def enterKey():
    #open a connection to the database
    conn = sqlite3.connect('DichotomousKey.db')

    #Ask user to enter the name of their key
    key = input("Enter a name for the key: ")
    print("")

    #create a new key node to hold the first node
    first = Nodes.KeyNode()

    #Ask user to enter the first question in the key
    first.text = input("Enter the first question: ")
    print("")

    #add first node to the database
    #add the first question into the Questions table
    sql = "INSERT INTO Questions (QuestionText) VALUES ('" + first.text + "');"
    id = Functions.addRow(conn, sql)

    #now insert a new row into the Nodes table, set first.id to the id of the row just inserted
    sql = "INSERT INTO Nodes (NodeType, NodeQuestion) VALUES ('Question', '" + str(id) +"');"
    first.id = Functions.addRow(conn, sql)

    #create a variable to hold current node, set it to first
    current = first 

    #create a new node and set current to the next node
    first.no = Nodes.KeyNode()
    current = first.no
    current.previous = first

    #add current to the database
    sql = "INSERT INTO Nodes (PreviousNode) VALUES (" + str(first.id) + ");"
    current.id = Functions.addRow(conn, sql)

    #update first in the database
    sql = "UPDATE Nodes SET NoNode = " + str(current.id) + " WHERE NodeID = " + str(first.id) + ";"
    conn.execute(sql)
    

    #loop through the tree while it is not full
    while(current != None):
        #first check if current is an empty node (if it is empty current will not have the attribute)
        if current.text is None:
            #if the node is empty:
            #print out the previous question and whether this node is the yes or no answer for it
            if current.previous.yes == current:
                print("Previous question: " + current.previous.text + " Answer: Yes")

            elif current.previous.no == current:
                print("Previous question: " + current.previous.text + " Answer: No")
            
            #ask the user if this node will hold a species or a question
            response = input("Will the current node hold a species? Y/N: ")
            print("")

            #if current is a species node
            if response.upper() == "Y":
                #set the scientific name
                current.text = input("What is the scientific name? ")
                print("")
                
                #check to see if the input species name already exists in species table
                #add a new species, using the scientific name provided, to species table
                sql = "INSERT INTO Species (ScientificNAme) VALUES ('" + current.text + "');"
                id = Functions.addRow(conn, sql)

                #update current in the database now
                #NodeType and NodeSpecies will be added, YesNode and NoNode will be left blank
                sql = "UPDATE Nodes SET NodeType = 'Species', NodeSpecies = " + str(id) + " WHERE NodeID = " + str(current.id) + ";"
                conn.execute(sql)

                #now move up a node
                current = current.previous

            #if current is not a species node
            elif response.upper() == "N":
                current.text = input("Enter the question that the current node will hold: ")
                print("")

                #add question to Questions table
                sql = "INSERT INTO Questions (QuestionText) VALUES ('" + str(current.text) + "');"
                id = Functions.addRow(conn, sql)

                #update node in database
                #NodeType and NodeQuestion will be added, YesNode and NoNode will be left blank
                sql = "UPDATE Nodes SET NodeType = 'Question', NodeQuestion = " + str(id) + " WHERE NodeID = " + str(current.id) +";"
                conn.execute(sql)

        #now, we need to move to the next node
        #check to see if the no pointer is empty
        if current.no is None:
            #create a new node and set the no pointer of current
            current.no = Nodes.KeyNode()

            #create new node in the database that has previous set to current
            sql = "INSERT INTO Nodes (PreviousNode) VALUES (" + str(current.id) + ");"
            current.no.id = Functions.addRow(conn, sql)

            #update current in the database
            sql = "UPDATE Nodes SET NoNode = " + str(current.no.id) + " WHERE NodeID = " + str(current.id) + ";"
            conn.execute(sql)

            #set previous of no pointer to current
            current.no.previous = current

            #now move current to no pointer
            current = current.no
        
        #if the no pointer is not empty, check to see if yes pointer is empty
        elif current.yes is None:
            #create a new node and set the yes pointer of current
            current.yes = Nodes.KeyNode()

            #create new node in the database that has previous set to current
            sql = "INSERT INTO Nodes (PreviousNode) VALUES (" + str(current.id) + ");"
            current.yes.id = Functions.addRow(conn, sql)

            #update current in the database
            sql = "UPDATE Nodes SET YesNode = " + str(current.yes.id) + " WHERE NodeID = " + str(current.id) + ";"
            conn.execute(sql)

            #set previous of yes pointer to current
            current.yes.previous = current

            #now move current to yes pointer
            current = current.yes
        
        #if neither pointer is empty, move up a node
        else:
            current = current.previous
    
    #outside of while loop    
    #add a new entry to the keys table with the keyname and first node
    sql = "INSERT INTO Keys (KeyName, FirstNode) VALUES ('" + str(key) + "', " + str(first.id) + ");"
    conn.execute(sql)

    #commit changes to the databse
    conn.commit()

    #close connection to the databse
    conn.close()

    print("Key created")
    return True

#function to fill up key using the database so that you can use the linked tree in python
def fillKey(key):
    #open a connection to the database
    conn = sqlite3.connect('DichotomousKey.db')
    db = conn.cursor()

    #get key info from the database
    sql = "SELECT FirstNode FROM Keys WHERE KeyID = " + str(key) + " ;"
    rows = db.execute(sql).fetchone()
    firstNodeID = rows[0]

    #create a new key node to hold the first node
    first = Nodes.KeyNode(id=firstNodeID)

    #create a variable to hold current node, set it to first
    current = first

    #loop through the tree while it is not full
    while(current != None):
        #first check if current is an empty node (if it is empty current will not have the attribute)
        if current.node_type is None:
            #if the node is empty:
            #get first node info from the database
            sql = "SELECT NodeType FROM Nodes WHERE NodeID = " + \
                str(current.id) + " ;"
            rows = db.execute(sql).fetchone()
            nodeType = rows[0]

            #set node type
            current.node_type = nodeType

            #if current is a species node
            if current.node_type == "Species":
                #get species ID from database
                sql = "SELECT NodeSpecies FROM Nodes WHERE NodeID = " + \
                    str(current.id) + " ;"
                rows = db.execute(sql).fetchone()
                speciesID = rows[0]

                #get species from database
                sql = "SELECT ScientificName FROM Species WHERE SpeciesID = " + \
                    str(speciesID) + " ;"
                rows = db.execute(sql).fetchone()

                #set text to species
                current.text = rows[0]

            #if current is not a species node
            elif current.node_type == "Question":
                #get question ID from database
                sql = "SELECT NodeQuestion FROM Nodes WHERE NodeID = " + \
                    str(current.id) + " ;"
                rows = db.execute(sql).fetchone()
                questionID = rows[0]

                #get question from database
                sql = "SELECT QuestionText FROM Questions WHERE QuestionID = " + \
                    str(questionID) + " ;"
                rows = db.execute(sql).fetchone()

                #set current text to question
                current.text = rows[0]

        #now, we need to move to the next node
        #check if node is a species, cannot keep filling after species
        if current.node_type == "Species":
            current = current.previous
        #check to see if the no pointer is empty
        elif current.no is None:
            #get no from database
            sql = "SELECT NoNode FROM Nodes WHERE NodeID = " + \
                str(current.id) + " ;"
            rows = db.execute(sql).fetchone()
            noNode = rows[0]

            #create a new node and set the no pointer of current, set previous to current
            current.no = Nodes.KeyNode(id=noNode, previous=current)

            #now move current to no pointer
            current = current.no

        #if the no pointer is not empty, check to see if yes pointer is empty
        elif current.yes is None:
            #get yes from database
            sql = "SELECT YesNode FROM Nodes WHERE NodeID = " + \
                str(current.id) + " ;"
            rows = db.execute(sql).fetchone()
            yesNode = rows[0]

            #create a new node and set the no pointer of current, set previous to current
            current.yes = Nodes.KeyNode(id=yesNode, previous=current)

            #now move current to yes pointer
            current = current.yes

        #if neither pointer is empty, move up a node
        else:
            current = current.previous

    #outside of while loop
    #close connection to the databse
    conn.close()

    return first

#TODO use fillKey at the beginning instead of keeping db connection open
#function to run a dichotomous key from the database
def runKey(key):
    #open a connection to the database
    conn = sqlite3.connect('DichotomousKey.db')

    #get the name of the key from the database
    sql = "SELECT KeyName FROM Keys WHERE KeyID = " + str(key) + " ;"
    rows = conn.execute(sql).fetchall()[0][0]

    #display the key name to the user
    print("Key: " + str(rows))
    print("")

    #get first node of the key from the database
    sql = "SELECT FirstNode FROM Keys WHERE KeyID = " + str(key) + " ;"
    rows = conn.execute(sql).fetchall()[0][0]

    #create a new key node to hold the first node
    first = Nodes.KeyNode()
    #set first id to the first node in the databse
    first.id = rows

    #get info about first node of the key from the database
    sql = "SELECT NoNode, YesNode FROM Nodes WHERE NodeID = " + str(first.id) + " ;"
    rows = conn.execute(sql).fetchall()[0]

    #set no of first
    nextNo = Nodes.KeyNode()
    nextNo.id = rows[0]
    first.no = nextNo

    #set yes of first
    nextYes = Nodes.KeyNode()
    nextYes.id = rows[1]
    first.yes = nextYes

    #set current to first node
    current = first

    #while noth yes and no pointers are not null
    while (current.no.id is not None) and (current.yes.id is not None):
        #get the question Id from the database
        sql = "SELECT NodeQuestion FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
        rows = conn.execute(sql).fetchall()[0][0]

        #get the question from the database
        sql = "SELECT QuestionText FROM Questions WHERE QuestionID = " +  str(rows) + " ;"
        rows = conn.execute(sql).fetchall()[0][0]

        #print the question
        response = input(str(rows) + " Y/N: ")

        #if repsonse is no
        if response.upper() == "N":
            #set current to no
            current = current.no

            #get info for current from database
            sql = "SELECT NoNode, YesNode FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
            rows = conn.execute(sql).fetchall()[0]

            #set no of current
            nextNo = Nodes.KeyNode()
            nextNo.id = rows[0]
            current.no = nextNo

            #set yes of current
            nextYes = Nodes.KeyNode()
            nextYes.id = rows[1]
            current.yes = nextYes

        #if repsonse is yes
        elif response.upper() == "Y":
            #set current to yes
            current = current.yes

            #get info for current from database
            sql = "SELECT NoNode, YesNode FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
            rows = conn.execute(sql).fetchall()[0]

            #set no of current
            nextNo = Nodes.KeyNode()
            nextNo.id = rows[0]
            current.no = nextNo

            #set yes of current
            nextYes = Nodes.KeyNode()
            nextYes.id = rows[1]
            current.yes = nextYes

    
    #after the while loop, get species
    sql = "SELECT NodeSpecies FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
    rows = conn.execute(sql).fetchall()[0][0]

    #get species info
    sql = "SELECT ScientificName FROM Species WHERE SpeciesID = " + str(rows) + " ;"
    rows = conn.execute(sql).fetchall()[0][0]

    #print out species info
    print("")
    print("Species: " + str(rows))

    #close connection to the databse
    conn.close()

#function to view all the keys in the database
def viewKeys():
    #open a connection to the database
    conn = sqlite3.connect('DichotomousKey.db')

    print("Keys currently in database")

    #get the name of all keys in keys table
    sql = "SELECT keyName FROM Keys"
    rows = conn.execute(sql).fetchall()

    #go through all the rows returned and print the name of each one
    ctr = 1
    for row in rows:
        print(str(ctr) + ". " + str(rows[ctr - 1][0]))
        ctr += 1

    #close connection to the databse
    conn.close()

#function to print out keys, allow a user to select one, then return the id of the selected key
def selectKey():
    #open a connection to the database
    conn = sqlite3.connect('DichotomousKey.db')

    #print out all keys in the database
    print("Keys currently in database")

    #get the name and ID of all keys in keys table
    sql = "SELECT keyName, keyID FROM Keys"
    rows = conn.execute(sql).fetchall()

    #go through all the rows returned and print the name of each one
    ctr = 1
    for row in rows:
        print(str(ctr) + ". " + str(rows[ctr - 1][0]))
        ctr += 1

    #ask user to select a key
    print("")
    response =  input("Type the number of the key you would like to run: ")
    print("")

    #get the id of the selected key
    key = rows[int(response) - 1][1]

    #close connection to the databse
    conn.close()

    #return the slected key id 
    return key

#function to delete a key and all nodes and questions (but NOT species) associated with it
#TODO fix this function (start by using fill key)
def deleteKey(key):
    #fill a linked list with the key from the database
    first = fillKey(key)

    #open a connection to the db so we can delete things from it
    conn = sqlite3.connect('DichotomousKey.db')
    db = conn.cursor()

    #set current node to first
    current = first

    #loop through while current is not none
    while(current != None):
        #if current is at the bottom of the tree, delete current
        if current.yes == None and current.no == None:
            # #if current is a question, we will have to delete the question associated with current first
            if current.node_type == "Question":

                #get the question id of the current node
                sql = "SELECT NodeQuestion FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
                rows = db.execute(sql).fetchone()
                question_id = rows[0]

                #delete the question fromt he questions table
                sql = "DELETE FROM Questions WHERE QuestionID = " + str(question_id) + " ;"
                db.execute(sql)
        
            # #delete the node from the db
            sql = "DELETE FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
            db.execute(sql)
            
            #before setting pointers, first check to see if this is the last node left
            if current.previous is None:
                #if so, set current to None
                current = None

            #set previous pointer to current to None
            elif current.previous.no == current:
                current.previous.no = None
                #set current to previous
                current = current.previous

            elif current.previous.yes == current:
                current.previous.yes = None
                #set current to previous
                current = current.previous

            #skip the rest of the loop and go back to the top
            continue
        
        #if current is not at the bottom of the tree, we need to walk to the bottom of the tree
        if current.no != None:
            current = current.no

        elif current.yes != None:
            current = current.yes

        else:
            current = current.previous

    #outside of while loop
    #delete the key from the keys table
    sql = "DELETE FROM Keys WHERE KeyID = " + str(key) + " ;"
    db.execute(sql)

    #commit the changes to the database and close
    conn.commit()
    conn.close()

    return True




    
deleteKey(2)