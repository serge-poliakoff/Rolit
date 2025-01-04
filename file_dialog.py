import os
from user_interface import *
from fltk import *

#constants:
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 580
MAX_WINDOW_HEIGHT = 800
BUTTON_HEIGHT = 25
#globals:
cur_path = os.path.realpath(__file__)
cur_path = cur_path[:cur_path.rindex('\\')]

class FileDialogButton(Button):
    hint_color = "#eeee55"
    standart_color = "#ffffff"
    icon = "folder-icon.gif"
    def __init__(self, t: str, coord_y: int, icon: str): #reduced constructor for a folder button
        self.icon = icon
        super().__init__(WINDOW_WIDTH, BUTTON_HEIGHT, t, self.standart_color , 0, coord_y)
        self.render()
    def render(self):
        rectangle(self.x,self.y,
                  self.x+self.width,self.y+self.height,
                    remplissage = self.color, couleur = self.color)
        image(self.height//3*2, self.y + self.height//3, self.icon, 
              self.height//5*4, self.height//5*4)
        texte(self.height//2*3 ,self.y,
              self.text, taille = (self.height//2))
        if (self.color !=self.standart_color): 
            self.color = self.standart_color
    def check_click(self, click_x: int, click_y: int) -> bool:
        return super().check_click(click_x, click_y)
    def action(self):
        global cur_path
        cur_path += "\\" + self.text
        super().action()
    
class BackButton(Button):
    hint_color = "#7878ff"
    standart_color = "#ffffff"
    icon = "undo-icon.gif"
    def __init__(self,coord_x, coord_y: int): #reduced constructor for a folder button
        super().__init__(BUTTON_HEIGHT//2*3, BUTTON_HEIGHT//3*2, "", self.standart_color , coord_x, coord_y)
        self.render()
    def render(self):
        rectangle(self.x,self.y,
                  self.x+self.width,self.y+self.height,
                    remplissage = self.color, couleur = self.color)
        if(self.color == self.standart_color):
            image(self.x, self.y, self.icon, 
              self.width, self.height, ancrage = 'nw')
        else: 
            self.color = self.standart_color
    def check_click(self, click_x: int, click_y: int) -> bool:
        return super().check_click(click_x, click_y)
    def action(self):
        global cur_path
        cur_path = cur_path[:cur_path.rindex('\\')]
        super().action()

def file_dialog_console():
    global cur_path
    while True:
        print("Current path: ", cur_path)
        content = os.listdir(cur_path)
        dirs = []
        files = []
        for ent in content:
            if os.path.isdir(cur_path + "\\" + ent):
                dirs.append(ent)
            else:
                files.append(ent)
        
        for dir in dirs: print(dir, " - ", "directory")
        for file in files: print("\t",file)

        act = input("Where would you go?")
        if act == "back":
            cur_path = cur_path[:cur_path.rindex('\\')]
        elif act in dirs:
            cur_path += "\\" + act
        elif act in files:
            return cur_path + "\\" + act
        else:
            print("Incomperhensible, please, try again")


def analyse_path(exts: list):
    global cur_path
    dirs = []
    files = []
    content = os.listdir(cur_path)
    als = len(exts)>0 and (exts[0] == '*')
    for ent in content:
        if os.path.isdir(cur_path + "\\" + ent):
            dirs.append(ent)
        else:
            if als or ent[ent.rindex('.'):] in exts:
                files.append(ent)
    return (dirs, files)

def file_dialog(exts: list):
    """
    A file dialog with a simple user interface
    param: exts - a list of possible file extensions (others would not show up on the screen)
    """
    global cur_path, WINDOW_WIDTH, WINDOW_HEIGHT, BUTTON_HEIGHT
    cree_fenetre(WINDOW_WIDTH,WINDOW_HEIGHT)
    path_pos_ch = (WINDOW_WIDTH - BUTTON_HEIGHT) // (BUTTON_HEIGHT//3)
    back_but = BackButton(WINDOW_WIDTH-BUTTON_HEIGHT*2, BUTTON_HEIGHT//10)
    fold_select = (exts[0] == "*")
    
    while True:
        efface_tout()
        rectangle(0,0,WINDOW_WIDTH,WINDOW_HEIGHT, remplissage = "white", couleur = "white")
        path_shown = "..." + cur_path[-1*path_pos_ch:]
        texte(0, 0, path_shown, taille = BUTTON_HEIGHT//2, ancrage = "nw")
        back_but.render()
        

        dnms, fnms = analyse_path(exts)
        content_h = (len(dnms) + len(fnms) + 4) * BUTTON_HEIGHT
        if WINDOW_HEIGHT < content_h:
            WINDOW_HEIGHT = content_h if content_h < MAX_WINDOW_HEIGHT else MAX_WINDOW_HEIGHT 
            redimensionne_fenetre(WINDOW_WIDTH, WINDOW_HEIGHT)
        dir_bts = [FileDialogButton(dnms[i], BUTTON_HEIGHT*(i+1), "folder-icon.gif") for i in range(len(dnms))]
        file_bts = [FileDialogButton(fnms[i], BUTTON_HEIGHT*(i+1+len(dnms)),"file-icon.gif") for i in range(len(fnms))]
        if fold_select:
            submit_but = Button(BUTTON_HEIGHT*4, BUTTON_HEIGHT, "Submit",
                        "#7788ff", WINDOW_WIDTH - BUTTON_HEIGHT*5, WINDOW_HEIGHT - BUTTON_HEIGHT - 10)
            submit_but.render()
        

        ev = attend_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            ferme_fenetre()
            break
        elif tev == 'ClicGauche':
            if back_but.check_click(abscisse(ev),ordonnee(ev)):
                mise_a_jour()
                continue
            if fold_select:
                if submit_but.check_click(abscisse(ev),ordonnee(ev)):
                    mise_a_jour()
                    ferme_fenetre()
                    return cur_path
            catched = False
            for but in dir_bts:
                catched = but.check_click(abscisse(ev),ordonnee(ev))
                if catched: break
            if not catched:
                for but in file_bts:
                    catched = but.check_click(abscisse(ev),ordonnee(ev))
                    if catched:
                        mise_a_jour()
                        ferme_fenetre()
                        return cur_path
                
            
        mise_a_jour()
    ferme_fenetre()

'''Examples of utilisation:

print(file_dialog(["*"])) - to select any file or folder

print(file_dialog([".csv",".json"])) - to select json or csv file

'''

