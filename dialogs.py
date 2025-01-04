from fltk import *
from buttons import *

TXT_SIZE = 15
WINDOW_W = 600
BUTTON_H = 40

def int_list_dialog(question: str, val_poss: list, default = 0):
    '''
    a function that creates a dialog menu via fltk and returns users response
    Arguments:
        question (str) - a question to user that will be affiched on top of the dialog window
        val_poss (list int) - a list of possible users responses. Would be presented as buttons on the screen
    '''
    global TXT_SIZE, WINDOW_W, BUTTON_H
    text_len = len(question) * TXT_SIZE
    if(text_len > WINDOW_W):
        WINDOW_W = text_len

    cree_fenetre(WINDOW_W, TXT_SIZE*2+BUTTON_H*(len(val_poss)+2))
    
    bts = [Button(WINDOW_W-80,BUTTON_H,str(val_poss[i]),"grey",40,TXT_SIZE*2+BUTTON_H*(i+1)) for i in range(len(val_poss))]
    while True:
        texte(WINDOW_W//2, TXT_SIZE ,
              question, ancrage = 'center', taille = TXT_SIZE)
        for but in bts:
            but.render()
        ev = attend_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            ferme_fenetre()
            return default
        elif tev == 'ClicGauche':
            but = None
            for but in bts:
                res = but.check_click(abscisse(ev), ordonnee(ev))
                if(res != False):
                    ferme_fenetre()
                    return res
            
        mise_a_jour()

'''
Example of ultilisation:

print(int_list_dialog("We'll need to confirm your age for this operation. How old are you?", [i for i in range(15,21)], 18))
'''

