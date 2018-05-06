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

""" Cette classe definit un projectile lance par le personnage """

from graphicgamecomponent import * # On importe la classe GraphicGameComponent (c'est un composant du jeu)

class Bullet(GraphicGameComponent) : # On herite la classe Bullet de GraphicGameComponent
    def __init__(self, vect = None, vel = 0, ground = None) : # Constructeur pouvant prendre en parametre le Canvas, le vecteur et la velocite
        GraphicGameComponent.__init__(self, ground) # On appelle le constructeur de GraphicGameComponent
        self.size = Size(5, 5) # On definit la taille : 5*5 px
        self.vect = vect # On conserve le vecteur
        self.vel = vel # On conserve la velocite

        self.imageBullet = PhotoImage(file="rc/images/bullet.gif") # On charge l'image
        self.rect = self.ground.create_image(self.pos.x, self.pos.y, anchor='nw', image=self.imageBullet) # On cree l'item graphique

    def draw(self) : # Cette fonction dessine le projectile | Cette fonction est surchargee.
        if self.ground : # Si le canvas est bien defini
            self.ground.coords(self.rect, self.pos.x, self.pos.y) # On actualise l'item

    def setOnTop(self) : # Cette fonction place l'item au premier plan | Cette fonction est surchargee.
        if self.ground : # Si le canvas est bien defini
            self.ground.tag_raise(self.rect) # On place l'item au premier plan

    def clear(self) : # Cette fonction permet de supprimer le projectile de l'affichage | Cette fonction est surchargee.
        if self.ground : # Si le canvas est bien defini
            self.ground.delete(self.rect) # On supprime les elements
