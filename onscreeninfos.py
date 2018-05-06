""" Cette classe definit l'affichage des infos a l'ecran """

from tkinter import font # On importe le module "font"

from threading import Timer # On importe le module Timer

from graphicgamecomponent import * # On importe la classe GraphicGameComponent (c'est un composant du jeu)

class OnScreenInfos(GraphicGameComponent) : # On herite la classe Platform de GraphicGameComponent
    def __init__(self, ground, size) : # Constructeur pouvant prendre en parametre le Canvas
        GraphicGameComponent.__init__(self, ground) # On appelle le constructeur de GraphicGameComponent
        self.size = size # On definit la taille

        self.animStepTime = .001 # Temps entre deux frames de l'animation

        font_bold = font.Font(family='Arial', size=12, weight='bold') # On cree une police d'ecriture grasse
        self.textItem = self.ground.create_text(5, 5, text="0", font=font_bold, anchor='nw') # On cree l'item texte

        font_bold = font.Font(family='Arial', size=16, weight='bold') # On cree une police d'ecriture grasse
        self.welcomeTextItem = self.ground.create_text(15, 150, text="Press the spacebar\nto start the game.\nUse the keys ← and → \nto control the player.\nLMB to fire gun.", font=font_bold, anchor='nw', fill="#ffffff") # On cree l'item texte
        self.ground.itemconfig(self.welcomeTextItem, state='hidden') # On cache l'item

        self.headerImage = PhotoImage(file="rc/images/header.gif") # On charge l'image
        self.headerImage = self.headerImage.zoom(size.width // self.headerImage.width(), 1) # On redimentionne l'image
        self.headerItem = self.ground.create_image(2, 0 , anchor='nw', image=self.headerImage) # On dessine l'image
        #self.ground.itemconfig(self.headerItem, state='hidden') # On cache l'item

        self.pauseImage = PhotoImage(file="rc/images/pause_button.gif") # On charge l'image
        self.pauseItem = self.ground.create_image(size.width - self.pauseImage.width() - 5, 0 , anchor='nw', image=self.pauseImage) # On dessine l'image
        self.ground.itemconfig(self.pauseItem, state='hidden') # On cache l'item

        self.gameOverImage = PhotoImage(file="rc/images/game_over.gif") # On charge l'image
        self.gameOverItem = self.ground.create_image(self.size.width / 2 - self.gameOverImage.width() / 2, size.height, anchor='nw', image=self.gameOverImage) # On dessine l'image
        self.ground.itemconfig(self.gameOverItem, state='hidden') # On cache l'item

        font_bold = font.Font(family='Arial', size=12, weight='bold') # On cree une police d'ecriture grasse
        self.statsText = self.ground.create_text(25, (self.size.height / 2), font=font_bold, anchor='nw', fill="#D6FCFF") # On cree l'item texte
        self.ground.itemconfig(self.statsText, state='hidden') # On cache l'item

    def setOnTop(self) : # Cette fonction permet de mettre tous les elements au premier plan
        self.ground.tag_raise(self.headerItem) # On force l'item a etre par dessus les autres graphismes
        self.ground.tag_raise(self.welcomeTextItem) # On force l'item a etre par dessus les autres graphismes
        self.ground.tag_raise(self.textItem) # On force l'item a etre par dessus les autres graphismes
        self.ground.tag_raise(self.pauseItem) # On force l'item a etre par dessus les autres graphismes
        self.ground.tag_raise(self.gameOverItem) # On force l'item a etre par dessus les autres graphismes
        self.ground.tag_raise(self.statsText) # On force l'item a etre par dessus les autres graphismes

    def setWelcomeTextVisibility(self, visible) : # Cette fonction permet d'afficher ou de masquer le texte de bienvenue
        if visible : # Si on a choisit visible
            self.ground.itemconfig(self.welcomeTextItem, state='normal') # On l'affiche
        else : # Si on a choisi chache
            self.ground.itemconfig(self.welcomeTextItem, state='hidden') # On le masque

    def setPoints(self, points) : # Cette fonction actualise le compte des points
        self.ground.itemconfig(self.textItem, text="{}".format(points)) # On modifie le texte en fonction des points

    def setPause(self, pause) : # Cette fonction actualise l'indicateur de pause
        if pause : # Si c'est en pause
            self.ground.itemconfig(self.pauseItem, state='hidden') # On le masque
        else : # Sinon
            self.ground.itemconfig(self.pauseItem, state='normal') # On l'affiche

    def gameOver(self, points, stats) : # Cette fonction affiche un message de fin
        self.ground.itemconfig(self.gameOverItem, state='normal') # On l'affiche

        # On cree le texte qui sera affiche
        text = "You're a looser ! :P\nYou got {} points.\n\nHere are your stats :\n- {} jumps on platforms\n- {} jumps on monsters\n- {} jumps on springs\n- {} jumps on trampolines\n- {} jumps on rockets\n- {} monsters shot".format(points, stats['platforms_jump'], stats['monsters_jump'], stats['springs_jump'], stats['trampolines_jump'], stats['rockets'], stats['monsters_shot'])

        # On applique le texte a l'item
        self.ground.itemconfig(self.statsText, text=text)

        self.setOnTop() # On met le tout au premier plan

        Timer(self.animStepTime, self.animGameOvertext).start() # On lance l'animation

    def animGameOvertext(self) : # Cette fonction permet l'animation du message "Game Over"
        if self.ground.coords(self.gameOverItem)[1] > self.size.height / 2 - self.gameOverImage.height() : # Tant que l'item n'a pas atteint la position desiree
            self.ground.coords(self.gameOverItem, self.ground.coords(self.gameOverItem)[0], self.ground.coords(self.gameOverItem)[1] - 20) # On actualise l'item

            Timer(self.animStepTime, self.animGameOvertext).start() # On lance une autre frame de l'animation
        else : # S'il a atteint la bonne position
            self.ground.itemconfig(self.statsText, state='normal') # On affiche les stats
