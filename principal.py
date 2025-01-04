from fltk import *
from regles import *
import dialogs
import time
from sauvegarde_parties import save_game

NOMBRE_PARTIES = 0
NOMBRE_J = 0
J = 0
scores_totaux = []
scores = []
size = 0

def col(num):
    if num == 0: return "#EEEEEE" # None 
    if num == 1: return "#00FF00" # Vert 
    if num == 2: return "#FF0000" # Rouge
    if num == 3: return "#FFFF00" # Jaune
    if num == 4: return "#0000FF" # Bleu

# Fonction pour vérifier si toutes les cases sont occupées
def verifier_fin_de_partie(a):
    for ligne in a:
        if 0 in ligne:  # Si une case est encore vide, la partie n'est pas finie
            return False
    return True

# Animation de fin de partie
def animation_fin_de_partie(a, size):
    couleurs = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"]
    for couleur in couleurs:
        for i in range(8):
            for j in range(8):
                rectangle(i * size, j * size, (i + 1) * size, (j + 1) * size, remplissage=couleur)
        mise_a_jour()
        time.sleep(0.3)

def demander_nombre_parties():
    """Demande à l'utilisateur combien de parties il veut jouer."""
    try:
        nb_parties = int(input("Combien de parties voulez-vous jouer ? "))
        if nb_parties < 1:
            print("Veuillez entrer un nombre valide supérieur à 0.")
            return demander_nombre_parties()
        return nb_parties
    except ValueError:
        print("Veuillez entrer un nombre entier.")
        return demander_nombre_parties()

def demander_nombre_joueurs():
    """Demande à l'utilisateur combien de parties il veut jouer."""
    try:
        nb_joueurs = int(input("Combien de joueurs ? "))
        if nb_joueurs < 2 or nb_joueurs > 4:
            print("Veuillez entrer un nombre valide entre 2 et 4.")
            return demander_nombre_joueurs()
        return nb_joueurs
    except ValueError:
        print("Veuillez entrer un nombre entier.")
        return demander_nombre_joueurs()

#creation de la fenetre 


def verefier_pas(a, x, y):
    """Vérifie si un mouvement est possible à la position (x, y)."""
    if a[x][y] != 0:
        return False
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if 0 <= i < len(a) and 0 <= j < len(a[0]) and a[i][j] != 0:
                return True
    return False


def vainqueur(scores):
    max_score = max(scores)  # Trouve le score maximum
    gagnants = []  # Liste pour stocker les gagnants

    # Trouve les joueurs avec le score maximum
    for i in range(len(scores)):
        if scores[i] == max_score:
            gagnants.append(i + 1)  # Ajoute le numéro du joueur (i + 1)

    # Affiche le ou les gagnants avec leur score
    print("Pour cette partie, le(s) vainqueur(s) est/sont :")
    for gagnant in gagnants:
        print("Joueur", gagnant, "avec un score de", max_score)



def mettre_a_jour_scores(a, NOMBRE_J):
    """Met à jour les scores en fonction de la grille actuelle."""
    scores_partie = [0] * NOMBRE_J  # Score pour cette partie uniquement
    # Parcourt la grille pour compter le nombre de cases de chaque joueur
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] != 0:  # Si la case est occupée
                scores_partie[a[i][j] - 1] += 1  # Met à jour le score pour cette partie

    # Ajoute les scores de cette partie aux scores cumulés
    ##for i in range(len(scores)):
    ##    scores[i] += scores_partie[i]
    
    # Affiche les scores pour cette partie
    print("Score pour cette partie :")
    for joueur, score in enumerate(scores_partie, 1):
        print(f"Joueur {joueur}: {score} cases")
    ##print(vainqueur(scores_partie))

    return scores_partie ## selon moi, ca a plus de sens voila pourquoi
                            ## imaginons par example qu'un joueur bleu a attrape une moitie de plateau
                            ## mais apres a ete completment detruit
                            ## dans ce cas, a la fin de partie il n'a presque pas de cases,
                            ## mais il peut egalement etre vainquer juste car il a tenu une moitie de plateau
                            ## au milieu de jeu, ce qui n'a aucun sens.
                            ## dans cette version seulement la distribution finale des cases est pris en consience



def gameplay():
    global scores_totaux
    for partie in range(NOMBRE_PARTIES):
        print(f"\nDébut de la partie {partie + 1}")
        
        # Initialisation de la grille et des scores pour la partie en cours
        a = [[0 for i in range(8)] for j in range(8)]
        scores = [0] * NOMBRE_J
        
        J = 0  # Le joueur qui doit jouer entre 0 et NOMBRE_J - 1
        PREMIERE_PAS_TRIGGER = True
        
        while True:
            # Affichage de la grille
            for i in range(8):
                for j in range(8):
                    rectangle(i * size, j * size, (i + 1) * size, (j + 1) * size, remplissage=col(a[i][j]))

            ev = attend_ev()
            tev = type_ev(ev)
            
            if tev == "ClicGauche":
                x = abscisse(ev) // size
                y = ordonnee(ev) // size
                if PREMIERE_PAS_TRIGGER or verefier_pas(a, x, y):
                    PREMIERE_PAS_TRIGGER = False
                    a[x][y] = J + 1
                    a = blockade(a, x, y)
                    scores = mettre_a_jour_scores(a, NOMBRE_J)
                    print("Scores actuels :", scores)
                    
                    # Vérifie si toutes les cases sont occupées après chaque coup
                    if verifier_fin_de_partie(a):
                        animation_fin_de_partie(a, size)
                        print("Fin de la partie", partie + 1, "! Scores pour cette partie :", scores)
                        
                        # Mise à jour des scores totaux avec les scores de la partie actuelle
                        scores_totaux = [scores_totaux[i] + scores[i] for i in range(NOMBRE_J)]
                        break  # Fin de la partie actuelle

                    # Passe au joueur suivant
                    J += 1
                    J %= NOMBRE_J
                    print("Coordonnées du coup :", x, y)

            elif tev == 'Quitte':  # Sort de la function gameplay
                ferme_fenetre()
                suvg = dialogs.int_list_dialog("Vous voulez sauvegarder ce jeu?",
                                               ["Oui", "Non"])
                if suvg == "Oui":
                    save_game(NOMBRE_J, J, NOMBRE_PARTIES, partie,
                        scores_totaux, scores, a)
                return

            mise_a_jour()




# Réinitialisation des scores pour une prochaine série de parties -> doit etre j'ai un peu mal compri a quoi ca serre
#scores_totaux = [0] * NOMBRE_J
#print("Scores réinitialisés pour une prochaine partie.")
def main():
    global NOMBRE_PARTIES, NOMBRE_J, J, scores_totaux, scores, size
    size = 60
    J = 0 
    NOMBRE_J = dialogs.int_list_dialog("Combien des jouers?", [2, 3, 4]) #nombre de joeurs dans partie
    NOMBRE_J = int(NOMBRE_J)
    if(NOMBRE_J == 0):
        quit()
    NOMBRE_PARTIES = dialogs.int_list_dialog("Combien de parties voulez-vous jouer ?", [1, 2, 3, 4])  # Nombre de parties
    NOMBRE_PARTIES = int(NOMBRE_PARTIES)
    if(NOMBRE_J == 0):
        quit()
    # Initialisation des scores totaux pour l'ensemble des parties
    scores_totaux = [0] * NOMBRE_J

    scores = [0] *NOMBRE_J

    cree_fenetre(size*8,size*8)
    x=0
    y=0
    PREMIERE_PAS_TRIGGER = True

    a = [ [0 for i in range(8)] for j in range(8)]      ##plateau de jeu

    gameplay()

    # Affiche les scores finaux après toutes les parties - faire en ecran
    print("\nScores totaux après", NOMBRE_PARTIES, "parties :", scores_totaux)
    vainqueur(scores_totaux)