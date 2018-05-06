"""
    This file is part of Space Jumper.

    Space Jumper is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Space Jumper is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Space Jumper.  If not, see <http://www.gnu.org/licenses/>. 2
"""

""" Cette classe est la base de tout element graphique du jeu, elle n'a pas pour but d'être instanciee mais d'être heritee """

from tkinter import * # On importe tout Tkinter au cas ou les classes filles en auraient besion

from graphictypes import * # On importe les types de variables propres au jeu (c'est un composant du jeu)

class GraphicGameComponent :
    def __init__(self, ground = None) : # Constructeur pouvant prendre en parametre le Canvas
        self.pos = Point(0, 0) # On cree une variable position par defaut
        self.drawOffset = Point(0, 0)
        self.size = Size(0, 0) # On cree une variable taille par defaut
        self.ground = ground # On stocke le Canvas

        self.attachedObject = None # Cette variable stocke l'objet attache
        self.attachedObjectOffset = Point(0, 0) # On peut lui appliquer un decalage

    def remove(self) : # Cette fonction permet de supprimer l'element de l'affichage.
        self.removeAttachedObject() # On supprime tout d'abord l'objet attache
        self.clear() # On supprime les graphismes

    def clear(self) : # Cette fonction permet de supprimer les graphismes. Cette fonction sera reimplementee dans les classes filles, donc vide ici
        pass

    def draw(self) : # Fonction de dessin. Cette fonction sera reimplementee dans les classes filles, donc vide ici
        pass

    def hit(self, object) : # Cette fonction est automatiquement appelee lorsqu'il y a une collision. Cette fonction sera reimplementee dans les classes filles, donc vide ici
        pass

    def fallOn(self, player) : # Cette fonction est automatiquement appelee lorsque le joueur tombe sur l'objet. Cette fonction sera reimplementee dans les classes filles, donc vide ici
        pass

    def move(self, point) : # Cette fonction permet de bouger l'element graphique a une position definie
        self.pos = point # On modifie la position actuelle
        self.draw() # On actualise l'affichage

        if self.attachedObject : # S'il y a un objet attache
            self.attachedObject.move(Point(point.x + (self.size.width / 2) - (self.attachedObject.size.width / 2)  + self.attachedObjectOffset.x, point.y - self.attachedObject.size.height + self.attachedObjectOffset.y)) # On actualise l'objet attache

    def translate(self, vect) : # Cette fonction permet de bouger l'element graphique par un vecteur defini
        self.move(self.pos + vect) # On bouge l'element en faisant la somme de sa position et du vecteur

    def resize(self, size) : # Cette fonction permet de redimensionner l'element graphique
        self.size = size # On modifie la taille actuelle
        self.draw() # On actualise l'affichage

    def setCanvas(self, ground) : # Cette fonction permet de changer de canvas
        self.ground = ground # On change de Canvas
        self.draw() # On actualise l'affichage

    def setOnTop(self) : # Cette fonction permet de passer l'element au premier plan. Cette fonction sera reimplementee dans les classes filles, donc vide ici
        pass

    def setAttachedObject(self, object, offset) : # Cette fonction permet d'attacher un objet. Elle prend en parametres l'objet a attacher et son decalage vertical
        self.attachedObject = object # On actualise la variable qui stocke l'objet
        self.attachedObjectOffset = offset # On actualise la variable qui stocke le decalage

        self.attachedObject.setParent(self) # On indique a l'objet attache que son parent est l'objet de la classe actuelle
        self.attachedObject.draw() # On le dessine

    def removeAttachedObject(self) : # Cette fonction supprime l'objet attache
        if self.attachedObject : # Si il a bien un objet attache
            self.attachedObject.remove() # On le supprime
            self.attachedObject = None # On reinitialise la variable a "None"

    def detachObject(self) : # Cette fonction detache l'objet attache sans le supprimer
        if self.attachedObject : # Si il a bien un objet attache
            self.attachedObject = None # On reinitialise la variable a "None
