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

""" Cette classe definit l'affichage des fonds parallax a l'ecran """

from graphicgamecomponent import * # On importe la classe GraphicGameComponent (c'est un composant du jeu)

class ParallaxBackground(GraphicGameComponent) : # On herite la classe Platform de GraphicGameComponent
    def __init__(self, ground, size, path, fact = 1) : # Constructeur pouvant prendre en parametre le Canvas, la taille, le chemin de l'image et le facteur de defilement
        GraphicGameComponent.__init__(self, ground) # On appelle le constructeur de GraphicGameComponent
        self.size = size # On definit la taille

        self.factor = fact # On stocke le facteur de defilement

        self.backgroundImage = PhotoImage(file=path) # On charge l'image
        self.bgSize = Size(self.backgroundImage.width(), self.backgroundImage.height()) # On stocke la taille d'une image seule

        self.tiles = [] # Cette liste contiendra toutes les "tuiles" du fond

        self.tilesCount = 3 # Par defaut, il y a 3 tuiles (minimum)

        if self.bgSize.height < self.size.height : self.tilesCount = (size.height // self.bgSize.height) + 1 # On calcule le bon nombre de tuiles

        for i in range(0, self.tilesCount) : # Pour chaque tuile necessaire
            tile = self.ground.create_image(0, i * self.bgSize.height, anchor='nw', image=self.backgroundImage) # On cree l'image
            self.tiles.append(tile) # On l'ajoute a la liste

    def setFactor(self, fact) : # Cette fonction permet de changer le facteur
        self.factor = fact # On stocke le facteur de defilement

    def scroll(self, yVect) : # Cette fonction fait defiler les tuiles (et donc le fond)
        yVect = int(yVect) # On s'assure que le vecteur vertical est un entier

        scroll = (yVect * self.factor) # On calcul de combien on doit defiler

        for i, tile in enumerate(self.tiles) : # Pour chaque tuile
            self.ground.coords(tile, 0, self.ground.coords(tile)[1] + scroll + 1) # On deplace la tuile

            if self.ground.coords(tile)[1] + scroll > self.size.height : # Si la tuile atteint le bas de l'ecran
                self.ground.coords(tile, 0, self.ground.coords(self.tiles[0])[1] - self.bgSize.height) # On la replace en haut
                del self.tiles[i] # On supprime la tuile en question
                self.tiles.insert(0, tile) # Et on la reinsere eu sommet de la liste
