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

""" Cette classe definit la plateforme la plus simple du jeu """

from graphicgamecomponent import * # On importe la classe GraphicGameComponent (c'est un composant du jeu)

class Platform(GraphicGameComponent) : # On herite la classe Platform de GraphicGameComponent
    def __init__(self, ground = None) : # Constructeur pouvant prendre en parametre le Canvas
        GraphicGameComponent.__init__(self, ground) # On appelle le constructeur de GraphicGameComponent
        self.size = Size(40, 20) # On definit la taille : 30x8 px
        self.needsToBeRemoved = False # Cette variable indique si la plateforme doit-etre supprimee

        self.photoimage = PhotoImage(file="rc/images/platform.gif") # On charge l'image

        if self.ground : # Si le canvas est bien defini
            #self.rect = self.ground.create_rectangle(self.pos.x, self.pos.y, self.pos.x + self.size.width, self.pos.y + self.size.height, fill="blue")
            self.rect = self.ground.create_image(2, 0, anchor='nw', image=self.photoimage) # On dessine l'image

    def clear(self) : # Cette fonction permet de supprimer la plateforme de l'affichage | Cette fonction est surchargee.
        if self.ground : # Si le canvas est bien defini
            self.ground.delete(self.rect) # On supprime les elements

    def draw(self) : # Cette fonction effectue le dessin de la plateforme dans le Canvas | Cette fonction est surchargee.
        if self.ground : # Si le Canvas est bien defini
            self.ground.coords(self.rect, self.pos.x + 2, self.pos.y) # On actualise le rectangle
