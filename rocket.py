""" Cette classe definit une fusee du jeu """

from attachedobject import * # On importe la classe AttachedObject (c'est un composant du jeu)

class Rocket(AttachedObject) : # On herite la classe AttachedObject
    def __init__(self, ground = None) : # Constructeur pouvant prendre en parametre le Canvas
        AttachedObject.__init__(self, ground) # On appelle le constructeur de AttachedObject
        self.size = Size(30, 73) # On definit la taille : 30*30 px
        self.drawOffset = Point(-5, -5)
        self.velYCoef = 5 # Coefficient de hauteur du saut provoque

        self.photoimage = PhotoImage(file="rc/images/rocket.gif") # On charge l'image

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

    def initDrawPlayer(self, player) : # Cette fonction initialise le proxy propre a la fusee
        player.ground.itemconfig(player.rect, state='hidden') # On chache l'image par defaut
        player.graphicItems.append(PhotoImage(file="rc/images/rocket_fire.gif")) # On charge l'image de la fusee
        player.graphicItems.append(player.ground.create_image(0, 0, anchor='nw', image=player.graphicItems[0])) # On cree l'item

        # Note: player.graphicItems permet de stocker des elements du proxy dans le personnage

    def drawPlayer(self, player) : # Cette fonction est la fonction de dessin par defaut
        if player.ground and len(player.graphicItems) == 2: # Si le Canvas est bien defini
            #self.ground.coords(self.rect, self.pos.x, self.pos.y, self.pos.x + self.size.width, self.pos.y + self.size.height) # On actualise le rectangle
            player.ground.coords(player.graphicItems[1], player.pos.x + self.drawOffset.x, player.pos.y + self.drawOffset.y - 50) # On actualise le rectangle
            player.ground.tag_raise(player.graphicItems[1]) # On force le rectangle a etre par dessus les autres graphismes

    def removeDrawPlayer(self, player) : # Cette fonction supprime le proxy
        for item in player.graphicItems : # Pour chaque item stocke
            player.ground.delete(item) # On le supprime

        del player.graphicItems[:] # On vide la liste

        player.ground.itemconfig(player.rect, state='normal') # Re-affiche l'image par defaut

    def setOnTop(self) : # Cette fonction place les elements au premier plan | Cette fonction est surchargee.
        self.ground.tag_raise(self.rect) # On force le rectangle a etre par dessus les autres graphismes

    def fallOn(self, player) : # Cette fonction est automatiquement appelee lorsque le joueur tombe sur l'objet | Cette fonction est surchargee.
        pass
