""" Cette classe est la base des objets attaches aux plateformes, elle n'a pas pour but d'être instanciee mais d'être heritee """

from graphicgamecomponent import * # On importe la classe GraphicGameComponent (c'est un composant du jeu)

class AttachedObject(GraphicGameComponent) : # On herite la classe AttachedObject de GraphicGameComponent
    def __init__(self, ground = None) : # Constructeur pouvant prendre en parametre le Canvas
        GraphicGameComponent.__init__(self, ground) # On appelle le constructeur de GraphicGameComponent
        self.parent = None # On initialise un parent nul

    def removeFromParent(self) : # Cette foncion supprime cet objet du parent
        if self.parent : # Si il a bien un parent
            self.parent.removeAttachedObject() # On demande de le supprimer

    def detachFromParent(self) : # Cette foncion detache cet objet du parent
        if self.parent : # Si il a bien un parent
            self.parent.detachObject() # On demande de le detacher

    def setParent(self, parent) : # Cette fonction sera appelee automatiquement et permet de definir le parent de l'objet attache
        self.parent = parent # On actualise la variable parent
