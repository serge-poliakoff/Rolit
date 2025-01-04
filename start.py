from dialogs import int_list_dialog as quest_dialog
from file_dialog import *
from principal import main as nouveau_jeu
from sauvegarde_parties import load_game

## lancer le jeu sauvegarder ou nouvelle
choix = quest_dialog("Bienvenue dans Rolit !",
                     ["Nouveau jeu", "Jeu sauvegarde"])
if choix == "Nouveau jeu":
    nouveau_jeu()
else:
    path = file_dialog([".rolit"])
    load_game(path)