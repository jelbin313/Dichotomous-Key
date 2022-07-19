import sqlite3

#create database function
def createDatabase():
        #connect to a database called data.db
        conn = sqlite3.connect('DichotomousKey.db')

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
