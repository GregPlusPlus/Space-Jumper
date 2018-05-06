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

""" Cette classe definit un monstre du jeu """

import random

from attachedobject import * # On importe la classe AttachedObject (c'est un composant du jeu)

class Monster(AttachedObject) : # On herite la classe AttachedObject
    def __init__(self, ground = None) : # Constructeur pouvant prendre en parametre le Canvas
        AttachedObject.__init__(self, ground) # On appelle le constructeur de AttachedObject
        self.size = None # On definit la taille
        self.drawOffset = Point(-5, -5) # On place l'image du monstre avec un decalage
        self.alive = True # Cette variable stocke l'etat de vie du monstre. Par defaut il est vivant
        self.velYCoef = 2.3 # Coefficient de hauteur du saut provoque

        self.photoimage = None # Variable qui stocke l'image

        # On choisit au hasard un des deux monstres
        if random.random() > .5 :
            self.photoimage = PhotoImage(file="rc/images/monster_1.gif") # On charge l'image
            self.size = Size(30, 45) # On applique la taille adequate
        else :
            self.photoimage = PhotoImage(file="rc/images/monster_2.gif") # On charge l'image
            self.size = Size(30, 22) # On applique la taille adequate

        if self.ground : # Si le canvas est bien defini
            # On cree un simple rectangle rouge
            #self.rect = self.ground.create_rectangle(self.pos.x, self.pos.y, self.pos.x + self.size.width, self.pos.y + self.size.height, fill="red")
            self.rect = self.ground.create_image(2, 0, anchor='nw', image=self.photoimage) # On dessine l'image

    def clear(self) : # Cette fonction permet de supprimer la plateforme de l'affichage | Cette fonction est surchargee.
        if self.ground : # Si le canvas est bien defini
            self.ground.delete(self.rect) # On supprime les elements

    def draw(self) : # Cette fonction effectue le dessin de la plateforme dans le Canvas | Cette fonction est surchargee.
        if self.ground : # Si le Canvas est bien defini
            #self.ground.coords(self.rect, self.pos.x, self.pos.y, self.pos.x + self.size.width, self.pos.y + self.size.height) # On actualise le rectangle
            if self.alive == False : # Si le monstre est mort
                self.pos.y += 10 # On augmente son ordonnee un peu plus, il va donc tomber et sera automatiquement supprime

            self.ground.coords(self.rect, self.pos.x, self.pos.y) # On actualise le rectangle
            self.setOnTop() # On force le monstre a etre au premier plan

    def setOnTop(self) : # Cette fonction place les elements au premier plan | Cette fonction est surchargee.
        self.ground.tag_raise(self.rect) # On force le rectangle a etre par dessus les autres graphismes

    def kill(self) : # Cette fontion actualise l'etat de vie du monstre
        self.alive = False # On actualise la variable
