"""
Construction de ficher de sauvegarde (.rolit):
NOMBRE_JOUEURS JOUER
NOMBRE_PARTIES PARTIE
<SCORES TOTAUX>
<SCRORES POUR CETTE PARTIE>
TAILLE_TABLEAUX
<TABLEAUX>
"""

import datetime

def to_str(*args):
    return ' '.join(map(str, args)) + "\n"

def load_game(path: str) -> None:
    with open(path, 'r') as f:
        nombre_j, j = map(int, f.readline().split())
        nombre_p, p = map(int, f.readline().split())
        scores_t = list(map(int, f.readline().split()))
        scores_p = list(map(int, f.readline().split()))
        n = int(f.readline())
        tableau = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            tableau[i] = list(map(int, f.readline().split()))
        print("Nombre jouers: ", nombre_j)
        print("En train de jouer: ", j)
        print("Nombre parties: ", nombre_p)
        print("Scores pour patries joues: ", *scores_t)
        print("Scores pour cette partie: ", *scores_p)
        ## lancer le jeu avec ces parametres
        ## reecrire la fonction gameplay de tel facon qu'on pourra l'employer ici
        print("tableau de jeu:")
        for i in range(n):
            print(*tableau[i])

def save_game(nombre_j:int, j:int, nombre_parties: int, partie: int,
              scores_t: list[int], scores_p: list[int], tableau: list[list]) -> None:
    name = str(datetime.date.today()) +".rolit"
    
    with open(name,'w') as f:
        f.write(to_str(nombre_j, j))
        f.write(to_str(nombre_parties, partie))
        f.write(to_str(*scores_t))
        f.write(to_str(*scores_p))
        f.write(to_str(len(tableau)))
        for i in range(len(tableau)):
            f.write(to_str(*tableau[i]))
    print("Successfully saved to .\\" + name)

''' Test
save_game(2, 1, 2, 0, [12, 10], [1, 5], [[1, 0, 1], [2, 2, 1], [0, 2, 1]])
load_game(str(datetime.date.today())+".rolit")
'''