import sqlite3

#connect to a database called data.db
conn = sqlite3.connect('DichotomousKey.db')
print("Successfully connected to database.")

sql = """CREATE TABLE Keys (
        KeyID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        KeyName TEXT NOT NULL,
        FirstNode INTEGER NOT NULL,
        FOREIGN KEY (FirstNode) REFERENCES Nodes(NodeID)
        );"""
conn.execute(sql)
print("Successfully created Keys table.")

sql = """CREATE TABLE Nodes (
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
print("Successfully created Nodes table.")

sql = """CREATE TABLE Questions (
            QuestionID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            QuestionText Text NOT NULL
        );"""
conn.execute(sql)
print("Successfully created Questions table.")

sql = """CREATE TABLE Species (
            SpeciesID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            ScientificName TEXT NOT NULL,
            CommonName TEXT,
            Description TEXT,
            Image TEXT
        );"""
conn.execute(sql)
print("Successfully created Species table.")

conn.commit()
conn.close()
