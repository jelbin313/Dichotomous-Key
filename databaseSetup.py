import sqlite3

#create database function
def createDatabase():
        #connect to a database called data.db
        conn = sqlite3.connect('DichotomousKey.db')

<<<<<<< HEAD
        sql = """CREATE TABLE IF NOT EXISTS Keys (
                KeyID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                KeyName TEXT NOT NULL,
                FirstNode INTEGER NOT NULL,
                FOREIGN KEY (FirstNode) REFERENCES Nodes(NodeID)
                );"""
        conn.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Nodes (
                NodeID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                PreviousNode INTEGER,
                YesNode INTEGER,
                NoNode INTEGER,
                NodeType TEXT CHECK (NodeType IN ('Question', 'Species')),
                NodeQuestion INTEGER,
                NodeSpecies INTEGER,
                FOREIGN KEY (NodeQuestion) REFERENCES Questions(QuestionID)
                FOREIGN KEY (NodeSpecies) REFERENCES Species(SpeciesID)
                );"""
        conn.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Questions (
                QuestionID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                QuestionText Text NOT NULL
                );"""
        conn.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Species (
                SpeciesID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ScientificName TEXT NOT NULL,
                CommonName TEXT,
                Description TEXT,
                Image TEXT
                );"""
        conn.execute(sql)

        conn.commit()
        conn.close()
=======
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
>>>>>>> 00b36401f8e7367fb3ec28b1f541d4da1215dfb2
