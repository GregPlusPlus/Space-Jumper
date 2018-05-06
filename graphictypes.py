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

""" Ces classes sont des types de variables facilitant la mise en oeuvre du jeu """

""" Classe Point qui definit une position (ou un vecteur) 2D """
class Point :
    def __init__(self, x, y) : # Constructeur de Point qui prend en parametre les coordonnees X et Y
        self.x = x
        self.y = y

    def __str__(self) : # Si on doit obtenir une chaine de caracteres
        return "Point({} , {})".format(self.x, self.y)

    def __repr__(self) : # Si on doit l'afficher
        return str(self)

    def __add__(self, other) : # Si on doit faire la somme
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other) : # Si on doit faire la difference
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other) : # Si on doit faire le produit par un autre Point
        return Point(self.x * other.x, self.y * other.y)

    """def __mul__(self, other) : # Si on doit faire le produit par un reel
        return Point(self.x * other, self.y * other)"""

""" Classe Size qui definit une taille 2D """
class Size :
    def __init__(self, w, h) : # Constructeur qui prend en parametre la longueur (width) et la hauteur (height)
        self.width = w
        self.height = h

    def __str__(self) : # Si on doit obtenir une chaine de caracteres
        return "Size({} , {})".format(self.width, self.height)

    def __repr__(self) : # Si on doit l'afficher
        return str(self)
