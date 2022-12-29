import sqlite3

#create database function
def createDatabase():
        #connect to a database called data.db
        conn = sqlite3.connect('DichotomousKey.db')

#open the sql file
with open('databaseSetup.sql', 'r') as sql_file:
    databaseSetup = sql_file.read()

#execute sql to create database
conn.executescript(databaseSetup)

#commit changes to databse
conn.commit()

#close connection to the database
conn.close()

print("Successfully created database.")
