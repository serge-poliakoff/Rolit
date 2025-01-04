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
        self.color = c
        self.x = coord_x
        self.y = coord_y

    def render(self):
        rectangle(self.x,self.y,
                  self.x+self.width,self.y+self.height,
                    remplissage = self.color)
        texte(self.x+self.width/2,self.y+self.height/2,
              self.text, ancrage = 'center', taille = (self.height//2))
        if (self.color !=self.standart_color): 
            self.color = self.standart_color ##used to only hint the button one frame after a click
    
    def check_click(self, click_x: int, click_y: int) -> bool:
        if click_x > self.x and click_x < (self.x + self.width):
            if click_y > self.y and click_y < (self.y + self.height):
                return self.action()
        return False
    
    def action(self):
        self.color = self.hint_color
        self.render()
        return self.text



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
            if(res != False)
                print("Click catched by " + res)
                break
        
    mise_a_jour()
ferme_fenetre()
"""