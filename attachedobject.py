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
