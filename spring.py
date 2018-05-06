""" Cette classe definit un ressort du jeu """

from attachedobject import * # On importe la classe AttachedObject (c'est un composant du jeu)

class Spring(AttachedObject) : # On herite la classe Spring de AttachedObject
    def __init__(self, ground = None) : # Constructeur pouvant prendre en parametre le Canvas
        AttachedObject.__init__(self, ground) # On appelle le constructeur de AttachedObject
        self.size = Size(34, 22) # On definit la taille : 30*30 px
        self.velYCoef = 1.8 # Coefficient de hauteur du saut provoque

        self.photoimage = PhotoImage(file="rc/images/spring.gif") # On charge l'image

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

            self.ground.coords(self.rect, self.pos.x, self.pos.y) # On actualise le rectangle
            self.setOnTop() # On force le monstre a etre au premier plan

    def setOnTop(self) : # Cette fonction place les elements au premier plan | Cette fonction est surchargee.
        self.ground.tag_raise(self.rect) # On force le rectangle a etre par dessus les autres graphismes

    def fallOn(self, player) : # Cette fonction est automatiquement appelee lorsque le joueur tombe sur l'objet | Cette fonction est surchargee.
        pass
