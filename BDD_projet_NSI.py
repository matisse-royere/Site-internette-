# Créé par agaupillat, le 08/02/2024 en Python 3.7

# coding: utf-8

import sqlite3

conn = sqlite3.connect('ma_base.db')

#Table Utilisateur
c=conn.cursor()
#c.execute("""DROP TABLE Utilisateur;""")
#c.execute("""DROP TABLE Fonction;""")
#c.execute("""DROP TABLE Connection;""")
#c.execute("""DROP TABLE Classe;""")

c.execute("""
CREATE TABLE IF NOT EXISTS Utilisateur(
     id_utilisateur INTEGER,
     nom TEXT,
     prenom TEXT,
     email VARCHAR,
     id_fonction INTEGER,
     id_connection INTEGER,
     id_classe INTEGER,
     UNIQUE ("email"),
     UNIQUE ("id_connection"),
     PRIMARY KEY ("id_utilisateur"),
     FOREIGN KEY ("id_fonction") REFERENCES "Fonction" ("id_fonction"),
     FOREIGN KEY ("id_connection") REFERENCES "Connection" ("id_connection"),
     FOREIGN KEY ("id_classe") REFERENCES "Classe" ("id_classe")
)""")

#Table Fonction
c.execute("""
CREATE TABLE IF NOT EXISTS Fonction(
     id_fonction INTEGER,
     fonction TEXT,
     PRIMARY KEY ("id_fonction")
)""")

#Table de connection(avec identifiant et mot de passe)
c.execute("""
CREATE TABLE IF NOT EXISTS Connection(
    id_connection INTEGER,
    mot_de_passe VARCHAR,
    PRIMARY KEY ("id_connection")
)""")

#Table Classe
c.execute("""
CREATE TABLE IF NOT EXISTS Classe(
    id_classe INTEGER,
    nom VACHAR,
    PRIMARY KEY ("id_classe")
    )""")

#Table Appel
c.execute("""
CREATE TABLE IF NOT EXISTS Appel(
    id_appel INTEGER,
    id_eleve INTEGER,
    statut BOOLEAN,
    date DATE,
    PRIMARY KEY ("id_appel"),
    UNIQUE ("id_eleve", "date"),
    FOREIGN KEY ("id_eleve") REFERENCES "Utilisateur" ("id_utilisateur")
)""")

try:
    Utilisateur = []
    Utilisateur.append((1,"SMITH","Mary","mary.smith%40gmail.com",2,1,None))
    Utilisateur.append((2,"TUM","Bob","bob.tum@gmail.com",2,2,None ))
    Utilisateur.append((3,"MOREAU","Adrien","adrien.moreau@gmail.com", 1, 3,None))
    c.executemany("""
    REPLACE INTO Utilisateur VALUES(?,?,?,?,?,?,?)""", Utilisateur)

    Fonction = []
    Fonction.append((1,"Eleve"))
    Fonction.append((2,"Professeurs"))
    Fonction.append((3,"Parent"))
    c.executemany("""
    INSERT INTO Fonction VALUES(?, ?)""", Fonction)

    Connection = []
    Connection.append((1,"mot_de_passe_1"))
    Connection.append((2,"mot_de_passe_2"))
    Connection.append((3,"adrien"))
    c.executemany("""
    INSERT INTO Connection VALUES(?, ?)""", Connection)

    Classe = []
    Classe.append((1,"Rookie"))
    Classe.append((2,"Medium"))
    Classe.append((3,"Pro"))
    Classe.append((4,"Expert"))
    c.executemany("""
    INSERT INTO Classe VALUES(?, ?)""", Classe)

    Appel = []
    Appel.append((1,3,False,"2024-03-10"))
    c.executemany("""
    INSERT INTO Appel VALUES(?, ?, ?, ?)""", Appel)

except sqlite3.IntegrityError as erreur : print(str(erreur))

conn.commit()

#conn.close()