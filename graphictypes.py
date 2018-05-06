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
