""" Cette classe definit la plateforme qui s'auto-detruit """

from threading import Timer # On importe le module Timer
import random # On importe le module random

from platform import * # On importe la classe Platform (c'est un composant du jeu)

class AutoDestructingPlatform(Platform) : # On herite la classe Platform de GraphicGameComponent
    def __init__(self, ground = None) : # Constructeur pouvant prendre en parametre le Canvas
        Platform.__init__(self, ground) # On appelle le constructeur de GraphicGameComponent

        if self.rect : # Si l'item existe bien
            self.photoimage = PhotoImage(file="rc/images/platform_autodestruct.gif") # On charge l'image
            self.ground.itemconfigure(self.rect, image=self.photoimage) # On affiche un personnage qui saute

        Timer(3 + random.random() * 2, self.autoDestruct).start() # On attend quelques temps puis la plateforme s'auto-detruit

    def autoDestruct(self) : # Cette fonction auto-detruit la plateforme
        self.needsToBeRemoved = True # Cette variable indique si la plateforme doit-etre supprimee
