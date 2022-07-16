import sqlite3
import Nodes
import Functions 

def enterKey():

    #open a connection to the database
    conn = sqlite3.connect('DichotomousKey.db')

    #Ask user to enter the name of their key
    key = input("Enter a name for the key: ")

    #create a new key node to hold the first node
    first = Nodes.KeyNode()

    #Ask user to enter the first question in the key
    first.text = input("Enter the first question: ")

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

            #if current is a species node
            if response == "Y":
                #set the scientific name
                current.text = input("What is the scientific name? ")
                
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
            elif response == "N":
                current.text = input("Enter the question that the current node will hold: ")

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

enterKey()

