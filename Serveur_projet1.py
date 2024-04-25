# Créé par amandinegaupillat, le 13/02/2024 en Python 3.7

#Serveur

import http.server
from BDD_projet_NSI import *

user_session = ()

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Classe utilisée pour recevoir, traiter et répondre à des requêtes HTTP"""

    def do_GET(self):
        """Méthode appelée quand un client envoie une requête GET, donc quand il veut consulter une page."""
        print ("SERVEUR: requête GET reçue")
        #L'attribut path contient le chemin indiqué dans l'url
        if self.path == '/':
            print ("SERVEUR: requête GET pour la racine")
            #On indique le chemin correspondant à la page démandée dans l'arborescence des fichiers
            self.path = 'CONNEXION.html'
        if self.path == '/inscription':
            print ("SERVEUR: requête GET pour la racine")
            #On indique le chemin correspondant à la page démandée dans l'arborescence des fichiers
            self.path = 'CREER_COMPTE.html'

        #permet d'accéder aà l'appel SEULEMENT SI c'est un prof
        if self.path == '/afficher':
            if user_session != None and user_session[1]==2 :
                print("Affichage des noms d'élève ")
                liste_eleve = "SELECT nom, prenom FROM Utilisateur"
                r=c.execute(liste_eleve).fetchall()
#permet d'afficher directement les noms dans l'appel
                with open("liste_eleve.html","w") as fichier :
                    fichier.write("<<table>")
                    for eleve in r:
                        fichier.write("<tr><td>"+eleve[0]+"</td>")
                        fichier.write("<td>"+eleve[1]+"</td>")
                        fichier.write('<td><input type="checkbox" id="person1" class="presence-checkbox"><label for="person1" class="presence-label"></label></td></tr>')
                    fichier.write("</table>")
                self.path="liste_eleve.html"
            else :
                self.path = 'EDT.html'

        #On appelle la méthode do_GET de la classe parente qui va envoyer la page en question au client
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


    def do_POST(self):
        """Méthode appelée quand un client envoie une requête POST, donc quand il envoie des données."""
        print ("SERVEUR: requête POST reçue pour l'URL /"+self.path)

        #on lit les données sous forme binaire
        content_length = int(self.headers['Content-Length'])
        post_data_bytes = self.rfile.read(content_length)
        print ("SERVEUR: Données reçues:\n", post_data_bytes)

        #on interprète les données comme du texte encodé selon la norme UTF-8
        post_data_str = post_data_bytes.decode("UTF-8")

        #on sépare chaque donnée
        list_of_post_data = post_data_str.split('&')

        #on construit un dictionnaire à partir des noms et des valeurs des données reçues
        post_data_dict = {}
        for item in list_of_post_data:
            variable, value = item.split('=')
            post_data_dict[variable] = value
        print ("SERVEUR: Données sous forme de dictionnaire:\n", post_data_dict)

        if self.path == '/verify':
            print('page methode = verify')
            #On peut maintenant traiter les données.
            #Ici, on va envoyer des pages différentes aux clients en fonction de leur connexion et informations personnelle
            Identifiant= post_data_dict['identifiant']
            mdp = post_data_dict['mot_de_passe']

            rch_user= 'SELECT id_utilisateur, email, mot_de_passe, id_fonction FROM Utilisateur AS U JOIN Connection AS F ON U.id_connection=F.id_connection WHERE email="'+Identifiant+'" AND mot_de_passe="'+mdp+'" '
            res = c.execute(rch_user).fetchone()
            print(sqlite3.Row,res)
            #variable globale indenté pour savoir qui est connecté
            user_session= (res[1],res[3])

            #test des conditions pour vérifier que l'utilisateur existe déjà dans la BDD
            #Si oui, affiche "ACCUEIL"  Sinon, affiche "Inscription"
            if res == None:
                print("reponse : None ")
                self.path = 'CONNEXION.html?msg=ERREUR'
            elif mdp != res[2]:
                print("reponse != mot de passe ")
                self.path = 'CONNEXION.html?msg=WRONG_MDP'
            else:
                print("reponse ==  mot de passe ")
                self.path = 'ACCUEIL.html'

#condition si l'utilisateur n'est pas inscrit et/ou veut s'inscrire
        if self.path == '/ajout':
            print('page methode = ajout')

            pseudo=post_data_dict['pseudo']
            email=post_data_dict['email']
            mdp=post_data_dict['mot_de_passe']
            Fonction=post_data_dict['fonction']

            c.execute("INSERT INTO Connection (mot_de_passe) VALUES(?)", (mdp,))
            print(c.lastrowid, sqlite3.Row)
            id_mdp = c.lastrowid

            Utilisateur= (pseudo, email, id_mdp, Fonction,)
            r = c.execute("INSERT INTO Utilisateur (pseudo, email, id_connection, id_fonction) VALUES(?,?,?,?,?)", Utilisateur)
            conn.commit()

            print(c.lastrowid)

            if r != None:
                print("Inscription effectuée : ",r)
                self.path ='Confirmation_Inscription.html'
            else:
                print("Erreur d'inscription")
                self.path ='CREER_COMPTE.html'

#condition pour récupéré les cases cochées dans le tableau d'appel
        if self.path == '/appel':
            print('page methode = appel')

#On instancie un serveur qui va écouter la boucle locale sur le port 8000
my_server = http.server.HTTPServer(('localhost', 8000), MyHttpRequestHandler)

#On démarre le serveur
#Il écoutera jusqu'à ce que le programme soit fermé.
try:
    my_server.serve_forever()
except: print("stop")

c.close()
conn.close()