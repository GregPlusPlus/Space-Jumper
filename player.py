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

""" Cette classe definit le personnage """
from math import * # On importe le module math

from threading import Timer # On importe le module Timer

from graphicgamecomponent import * # On importe la classe GraphicGameComponent (c'est un composant du jeu)
from bullet import * # On importe la classe Bullet (c'est un composant du jeu)

class Player(GraphicGameComponent) : # On herite la classe Player de GraphicGameComponent
    def __init__(self, ground = None) : # Constructeur pouvant prendre en parametre le Canvas
        GraphicGameComponent.__init__(self, ground) # On appelle le constructeur de GraphicGameComponent
        self.size = Size(30, 84) # On definit la taille : 30*84 px
        self.drawOffset = Point(-5, 0)
        self.inGamePos = Point(0, 0) # On initialise sa position dans l'espace du jeu
        self.jump = False # On initialise la variable qui indique si il est en train de sauter. Par defaut il ne l'est pas
        self.alive = True # Cette variable stocke l'etat de vie du joueur, par defaut il est vivant
        self.hittable = True # Cette variable dit si le personnage repond aux collisions
        self.flying = False # Cette variable dit si le personnage est en train de voler
        self.flyingSpeed = 0  # Cette variable donne la vitesse de vol du personnage
        self.flyingFramesCount = 0 # Cette variable stocke la longueur u vol (en nombre de frames)
        self.flyingOrigin = -1 # Cette variable stocke ce qui est à l'origine du saut
        self.velY = 0 # Cette variable stocke la velocite verticale
        self.velX = 0 # Cette variable stocke la velocite horizontale (un peu inutile au final... :-| )

        self.bullets = [] # Cette liste contiendra les projectiles lances

        self.graphicItems = [] # Cette liste ne sert qu'aux proxys pour stocker leur items
        self.proxyDrawFunc = self.defDraw # La variable "proxyDrawFunc" est un pointeur sur une fonction qui permet de dessiner le personnage
                                      # Ainsi, il y a possibilite d'assigner au personnage une autre fonction de dessin et qui
                                      # peut-etre modifiee par un autre element du jeu en fonction des besoins.
                                      # Par defaut, "proxyDrawFunc" est initialisee avec la fonction "self.defDraw"
                                      # Aussi, la fonction stockee dans "proxyDrawFunc" prend en parametre une variable qui est une reference sur
                                      # le personnage. Cette reference est passee en argument a la fonction grace a la ligne "self.proxyDrawFunc(self)"
                                      # dans la fonction "draw".
                                      # Note: La fonction pointee peut acceder a toutes les variables membres du personnage.
        self.removeProxyDrawFunc = None  # La variable "proxyDrawFunc" est un pointeur sur une fonction qui permet de reinitialiser le proxy

        self.photoimageAlive = PhotoImage(file="rc/images/player.gif") # On charge l'image
        self.photoimageDead = PhotoImage(file="rc/images/player_dead.gif") # On charge l'image
        self.photoimageJumping = PhotoImage(file="rc/images/player_jumping.gif") # On charge l'image

        if self.ground : # Si le canvas est bien defini
            # On cree un simple rectangle rouge
            #self.rect = self.ground.create_rectangle(self.pos.x, self.pos.y, self.pos.x + self.size.width, self.pos.y + self.size.height, fill="red")
            self.rect = self.ground.create_image(0, 0, anchor='nw', image=self.photoimageAlive) # On dessine l'image

    def clear(self) : # Cette fonction permet de supprimer la plateforme de l'affichage | Cette fonction est surchargee.
        if self.ground : # Si le canvas est bien defini
            self.ground.delete(self.rect) # On supprime les elements

    def draw(self) : # Cette fonction effectue le dessin de la plateforme dans le Canvas | Cette fonction est surchargee.
        self.proxyDrawFunc(self) # Appel de la fonction stockee dans le pointeur "proxyDrawFunc"

    def setProxyDraw(self, init, func, remove) : # Cette fonction permet d'assigner un proxy
        self.removeProxyDrawFunc = remove # On stocke le bon pointeur

        #self.ground.itemconfig(self.rect, state='hidden')

        if init : # Si la fonction "init" est specifiee
            init(self) # On l'appelle

        self.proxyDrawFunc = func # On stocke le bon pointeur

        self.draw() # On redessine le personnage

    def removeProxyDraw(self) : # Cette fonction permet de supprimer le proxy
        self.removeProxyDrawFunc(self) # On supprime le proxy
        self.proxyDrawFunc = self.defDraw # On reinitialise la fonction de dessin par defaut

        self.draw() # On redessine le personnage

    def defDraw(self, player) : # Cette fonction est la fonction de dessin par defaut
        if player.ground : # Si le Canvas est bien defini
            #self.ground.coords(self.rect, self.pos.x, self.pos.y, self.pos.x + self.size.width, self.pos.y + self.size.height) # On actualise le rectangle
            player.ground.coords(player.rect, player.pos.x + self.drawOffset.x, player.pos.y + self.drawOffset.y) # On actualise le rectangle

    def setOnTop(self) : # Place le joueur au premier plan | Cette fonction est surchargee.
        self.ground.tag_raise(self.rect) # On force le rectangle a etre par dessus les autres graphismes

    def setJump(self, isJumping) : # On actualise l'etat du joueur s'il saute
        self.jump = isJumping # On actualise l'etat
        self.draw() # On actualise l'affichage

    def setVelY(self, velY) : # Cette fonction definit la velocite horizontale du joueur
        self.velY = velY # On actualise la variable
        #self.draw() # On actualise le dessin a l'ecran (pas sur de l'interet ici, a voir si c'est a supprimer)

    def setVelX(self, velX) : # Cette fonction definit la velocite verticale du joueur (un peu inutile dans notre cas)
        self.velX = velX
        self.draw() # On actualise le dessin a l'ecran (pas sur de l'interet ici, a voir si c'est a supprimer)

    # ====== Les fonction suivantes ne sont que des accesseurs ====== #

    def setHittable(self, h) :
        self.hittable = h

    def setFlying(self, f) :
        self.flying = f

    def setFlyingFrameCount(self, fc) :
        self.flyingFramesCount = fc

    def setFlyingSpeed(self, s) :
        self.flyingSpeed = s

    def setFlyingOrigin(self, o) :
        self.flyingOrigin = o

    # =============================================================== #

    def fly(self, fly, fc, s, o) : # Cette fonction permet de faire voler le personnage
        self.setHittable(not fly)    # On actualise les parametres de vol
        self.setFlying(fly)          # On actualise les parametres de vol
        self.setFlyingFrameCount(fc) # On actualise les parametres de vol
        self.setFlyingSpeed(s)       # On actualise les parametres de vol
        self.setFlyingOrigin(o)      # On actualise les parametres de vol

    def kill(self) : # Cette fonction permet de tuer le personnage
        self.alive = False # On actualise la variable
        self.ground.itemconfigure(self.rect, image=self.photoimageDead) # On affiche un personnage mort
        self.draw() # On le re-dessine si besoin

    def jumpAnimation(self) : # Cette fonction est appelee quand le personnage saute (inutilisee au final)
        self.ground.itemconfigure(self.rect, image=self.photoimageJumping) # On affiche un personnage qui saute
        Timer(.3, self.endJumpAnimation).start() # On attend quelques temps... Puis on remet l'image originale

    def endJumpAnimation(self) : # Cette fonction est appellee une fois que "l'animation" de saut est finie
        if self.alive : # Si le personnage toujours vivant
            self.ground.itemconfigure(self.rect, image=self.photoimageAlive) # On affiche un personnage "normal"

    def shot(self, vect) : # Cette fonction fait tirer un coup de feu
        mod = sqrt(vect.x**2 + vect.y**2)        # |--> On normalise le vecteur
        vect = Point(vect.x / mod, vect.y / mod) # |

        bullet = Bullet(vect, 10, self.ground) # On cree un projectile
        bullet.move(Point(self.pos.x + self.size.width / 2, self.pos.y)) # On le place en haut au milieu du personnage
        bullet.setOnTop() # On s'assure que le projectile est au dessus du reste

        self.bullets.append(bullet) # On l'ajoute a la liste des Projectiles
