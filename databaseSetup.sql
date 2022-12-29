CREATE TABLE IF NOT EXISTS Keys (
        KeyID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        KeyName TEXT NOT NULL,
        FirstNode INTEGER NOT NULL,
        FOREIGN KEY (FirstNode) REFERENCES Nodes(NodeID)
        );

CREATE TABLE IF NOT EXISTS Nodes (
            NodeID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            PreviousNode INTEGER,
            YesNode INTEGER,
            NoNode INTEGER,
            NodeType TEXT CHECK (NodeType IN ('Question', 'Species')),
            NodeQuestion INTEGER,
            NodeSpecies INTEGER,
            FOREIGN KEY (NodeQuestion) REFERENCES Questions(QuestionID)
            FOREIGN KEY (NodeSpecies) REFERENCES Species(SpeciesID)
        );

CREATE TABLE IF NOT EXISTS Questions (
            QuestionID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            QuestionText Text NOT NULL
        );

CREATE TABLE IF NOT EXISTS Species (
            SpeciesID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            ScientificName TEXT NOT NULL,
            CommonName TEXT,
            Description TEXT,
            Image TEXT
        );