import sqlite3
import Nodes
import Functions 

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

def deleteKey(key):
    #open a connection to the database
    conn = sqlite3.connect('DichotomousKey.db')
    db = conn.cursor()

    #get key info from the database
    sql = "SELECT KeyName, FirstNode FROM Keys WHERE KeyID = " + str(key) + " ;"
    rows = db.execute(sql).fetchone()
    keyName = rows[0]
    firstNodeID = rows[1]

    #display the key name to the user, give them a chnace to confirm
    response = input("Are you sure you want to delete " + str(keyName) + " Y/N:")

    #if the user does not want to delete the key, return from this function
    if response.upper() == "N":
        return

    #get first node info from the database
    sql = "SELECT YesNode, NoNode, NodeType FROM Nodes WHERE NodeID = " + str(firstNodeID) + " ;"
    rows = db.execute(sql).fetchone()
    yesNode = rows[0]
    noNode = rows[1]
    nodeType = rows[2]

    #create a key node to hold the first node, add attributes from database
    first = Nodes.KeyNode(id=firstNodeID, yes=yesNode, no=noNode, node_type=nodeType)

    #create a variable to hold current node, set it to first
    current = first

    #now that we are at the bottom of the key, we can start deleting
    while(current is not None):
        #go to the bottom and left most (no most) node
        while(current.no is not None) or (current.yes is not None):
            #if no contains a node we will be moving to no
            if current.no is not None:
                #if type is int, we will need to populate the node first
                if(type(current.no) == int):
                    #get the current node's no node
                    sql = "SELECT YesNode, NoNode, NodeType FROM Nodes WHERE NodeID = " + str(current.no) + " ;"
                    rows = db.execute(sql).fetchone()
                    yesNode = rows[0]
                    noNode = rows[1]
                    nodeType = rows[2]

                    #create a new key node to hold the first node, add attributes from database
                    current.no = Nodes.KeyNode(id=current.no, yes=yesNode, no=noNode, node_type=nodeType)

                #set previous
                current.no.previous = current

                #set current to current.no
                current = current.no

            #if no does not contain a node, check yes
            elif current.yes is not None:
                #if type is int, we will need to populate the node first
                if(type(current.no) == int):
                    #get the current node's yes node
                    sql = "SELECT YesNode, NoNode, NodeType FROM Nodes WHERE NodeID = " + \
                        str(current.yes) + " ;"
                    rows = db.execute(sql).fetchone()
                    yesNode = rows[0]
                    noNode = rows[1]
                    nodeType = rows[2]

                    #create a new key node to hold the first node, add attributes from database
                    current.yes = Nodes.KeyNode(id=current.yes, yes=yesNode, no=noNode, node_type=nodeType)

                #set previous
                current.yes.previous = current

                #set current to current.no
                current = current.yes

        #now delete current node
        #if the node is a question node, delete the question
        #species do not get deleted, they can be used in mutliple keys
        if current.node_type == "Question":
            #get question node from database
            sql = "SELECT NodeQuestion FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
            rows = db.execute(sql).fetchone()

            #now delete the questiom from the questions table
            sql = "DELETE FROM Questions WHERE QuestionID =" + str(rows[0]) + " ;"
            print(sql)
            db.execute(sql)
        
        #now delete the current node from the db
        sql = "DELETE FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
        print(sql)
        db.execute(sql)

        print(current.id)
        print(current.previous)

        #now set whatever points to the current node to none
        if current.previous.no == current:
            current.previous.no = None
        elif current.previous.yes == current:
            current.previous.yes = None

        #now move to previous node
        current = current.previous


         
    # #now delete the key from the keys table
    sql = "DELETE FROM Keys WHERE KeyID = " + str(key) +" ;"
    print(sql)
    db.execute(sql)

    # #commit changes to the databse
    # #conn.commit()

    #close connection to the databse
    conn.close()

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
        print(current)
        print(current.id)
        print("node type: " + str(current.node_type))
        #first check if current is an empty node (if it is empty current will not have the attribute)
        if current.node_type is None:
            #if the node is empty:
            #get first node info from the database
            sql = "SELECT NodeType FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
            rows = db.execute(sql).fetchone()
            nodeType = rows[0]

            #set node type
            current.node_type = nodeType
            print("node type: " + str(current.node_type))
            
            #if current is a species node
            if current.node_type == "Species":
                #get species ID from database
                sql = "SELECT NodeSpecies FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
                rows = db.execute(sql).fetchone()
                speciesID = rows[0]

                #get species from database
                sql = "SELECT ScientificName FROM Species WHERE SpeciesID = " + str(speciesID) + " ;"
                rows = db.execute(sql).fetchone()

                #set text to species
                current.text = rows[0]

            #if current is not a species node
            elif current.node_type == "Question":
                #get question ID from database
                sql = "SELECT NodeQuestion FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
                rows = db.execute(sql).fetchone()
                questionID = rows[0]

                #get question from database
                sql = "SELECT QuestionText FROM Questions WHERE QuestionID = " + str(questionID) + " ;"
                rows = db.execute(sql).fetchone()

                #set current text to question
                current.text = rows[0]

        print("text: ", current.text)
        print("no: ", current.no)
        print("yes: ", current.yes)
        print("previous: ", current.previous)

        #now, we need to move to the next node
        #check if node is a species, cannot keep filling after species
        if current.node_type == "Species":
            print("current moved to previous", current.previous)
            current = current.previous
        #check to see if the no pointer is empty
        elif current.no is None:
            #get no from database
            sql = "SELECT NoNode FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
            rows = db.execute(sql).fetchone()
            noNode = rows[0]

            #create a new node and set the no pointer of current, set previous to current
            current.no = Nodes.KeyNode(id=noNode, previous=current)

            print("current moved to no", current.no, current.no.id)


            #now move current to no pointer
            current = current.no

        #if the no pointer is not empty, check to see if yes pointer is empty
        elif current.yes is None:
            #get yes from database
            sql = "SELECT YesNode FROM Nodes WHERE NodeID = " + str(current.id) + " ;"
            rows = db.execute(sql).fetchone()
            yesNode = rows[0]

            #create a new node and set the no pointer of current, set previous to current
            current.yes = Nodes.KeyNode(id=yesNode, previous=current)

            print("current moved to yes", current.yes, current.yes.id)

            #now move current to yes pointer
            current = current.yes

        #if neither pointer is empty, move up a node
        else:
            print("current moved to previous", current.previous)

            current = current.previous

        print(" ")

    #outside of while loop
    #close connection to the databse
    conn.close()

    print("Key filled")
    return first

    
