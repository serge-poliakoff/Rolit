from fltk import *


class Button:
    x = 0
    y = 0
    width = 100
    height = 40
    text = "Button"
    color = "grey"
    hint_color = "red"
    standart_color = "grey"

    def __init__(self, w: int, h: int, t: str, c: str, coord_x: int, coord_y: int):
        self.width = w
        self.height = h
        self.text = t
        self.standart_color = self.color = c
        self.x = coord_x
        self.y = coord_y

    def render(self, text_anc = 'center'):
        rectangle(self.x,self.y,
                  self.x+self.width,self.y+self.height,
                    remplissage = self.color)
        texte(self.x+self.width/2,self.y+self.height/2,
              self.text, ancrage = text_anc, taille = (self.height//2))
        if (self.color !=self.standart_color): 
            self.color = self.standart_color ##used to only hint the button one frame after a click
    
    def check_click(self, click_x: int, click_y: int) -> bool:
        if click_x > self.x and click_x < (self.x + self.width):
            if click_y > self.y and click_y < (self.y + self.height):
                self.action()
                return True
        return False
    
    def action(self):
        self.color = self.hint_color
        self.render()




"""
 Main buttons bibliotheque
 Includes (meant to be abstract, but this doesn't exist in "this beautiful language")
 Button class that represents a structure that unies all the standart button attributes:
    x and y for the coordinates of left-top corner
    width and height (comperhensible, i suppose...)
    standart_color for a color of inaffected button
    and hint_color is a colored button would be colored one frame after catching a click
And methods:
    render() -> to invoque every frame to affiche a button on the screen
    check_click(int x, int y) -> to check if click on (x, y) coordinates touches that button, if true, returns true and calls an action method
    action() -> meant to be completed in the children classes, for this only recolors the button in a hinted color
To fully understand this bibliotheque workflow, example of utilisation is suggested:

 --- example d'utilisation ---
cree_fenetre(320,100)
bts = [Button(25,20,"b"+str(i),"grey",32*i,20) for i in range(1,8)]
while True:
    for but in bts:
        but.render()
    ev = attend_ev()
    tev = type_ev(ev)
    if tev == "Quitte":
        ferme_fenetre()
        break
    elif tev == 'ClicGauche':
        but = None
        for but in bts:
            res = but.check_click(abscisse(ev), ordonnee(ev))
            if(res != False):
                print("Click catched by " + but.text)
                break
        
    mise_a_jour()
ferme_fenetre()
"""


class TextField:
    label = "field: "
    text = ""
    focused = False

    x = 0
    y = 0
    width = 200
    height = 20
    unfoc_color = "#dfdfdf"
    foc_color = "#6090ff"
    inner_color = "#ffffff"
    col = unfoc_color

    def __init__(self, x: int, y: int, label: str, w = 200, h = 20,
                 unf_col = "#888888", foc_col = "#6090ff", in_col = "#ffffff"):
        self.x = x
        self.y = y
        self.label = label
        self.width = w
        self.height = h
        self.foc_color = foc_col
        self.unfoc_color = self.col = unf_col
        self.inner_color = in_col
        self.focused = False

    def render(self):
        texte(self.x, self.y, self.label, ancrage = "ne", taille = self.height//2)
        rectangle(self.x,self.y,
                self.x+self.width,self.y+self.height,
                remplissage = self.inner_color, couleur = self.col)
        texte(self.x+self.width//15,self.y+self.height//10,
              self.text, taille = (self.height//2))
    
    def check_click(self, click_x: int, click_y: int):
        if click_x > self.x and click_x < (self.x + self.width) and click_y > self.y and click_y < (self.y + self.height):
            self.focused = True
            self.col = self.foc_color
        else:
            self.focused = False
            self.col = self.unfoc_color
            
    
    def consume_text(self, text: str):
        if len(text) == 0:
            self.text = ""
            return
        if not self.focused: return

        self.text += text
    
    def backspace(self):
        if not self.focused: return

        if(len(self.text)>0):
            self.text = self.text[:-1]
    
    def enter(self):
        if not self.focused: return

        res = self.text
        self.focused = False
        self.col = self.unfoc_color
        return res
    
        

'''
cree_fenetre(320,100)
field = TextField(10,10, 200, 20)
while True:
    field.render()
    ev = attend_ev()
    tev = type_ev(ev)
    if tev == "Quitte":
        ferme_fenetre()
        break
    elif tev == 'ClicGauche':
        field.check_click(abscisse(ev), ordonnee(ev))
    elif tev == 'Touche':
        print(touche(ev))
        if len(touche(ev)) == 1: field.consume_text(touche(ev))
        elif touche(ev) == 'space': field.consume_text(" ")
        elif touche(ev) == 'BackSpace': field.backspace()
        elif touche(ev) == 'Return':
            print(field.enter())         
    mise_a_jour()

ferme_fenetre()
'''