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

""" Cette classe est la classe principale du jeu. C'est ici qu'ont lieu les interactions """

from tkinter import Tk, Canvas, messagebox # On importe les modules Tk necessaires
import random # On importe le module random
from math import * # On importe le module math
import datetime # On importe le module datetime

from gameconsts import *              # On importe la classe CONSTS (c'est un composant du jeu)
from platform import *                # On importe la classe Platform (c'est un composant du jeu)
from autodestructingplatform import * # On importe la classe AutoDestructingPlatform (c'est un composant du jeu)
from player import *                  # On importe la classe Player (c'est un composant du jeu)
from monster import *                 # On importe la classe Monster (c'est un composant du jeu)
from spring import *                  # On importe la classe Spring (c'est un composant du jeu)
from trampoline import *              # On importe la classe Trampoline (c'est un composant du jeu)
from collisionmanager import *        # On importe la classe CollisionManager (c'est un composant du jeu)
from onscreeninfos import *           # On importe la classe OnScreenInfos (c'est un composant du jeu)
from parallaxbackground import *      # On importe la classe OnScreenInfos (c'est un composant du jeu)
from rocket import *                  # On importe la classe Rocket (c'est un composant du jeu)
from bullet import *                  # On importe la classe Bullet (c'est un composant du jeu)
from soundmanager import *            # On importe la classe SoundManager (c'est un composant du jeu)
from scoresmanager import *           # On importe la classe ScoresManager (c'est un composant du jeu)
from scoresdialog import *            # On importe la classe ScoresDialog (c'est un composant du jeu)
from aboutdialog import *             # On importe la classe AboutDialog (c'est un composant du jeu)

class Game(Tk): # On herite la classe Game de Tk
    def __init__(self, wsize) : # Constructeur qui prend la taille de la fenetre en parametre
        Tk.__init__(self) # Constructeur de la fenetre Tk

        self.resizable(width=False, height=False) # la fenetre a une taille fixe
        self.title("Space Jumper") # On renomme la fenetre

        self.size = wsize # Variable qui stocke la taille de la fenetre

        self.buildGUI() # On initialise l'interface graphique

        self.initObjects() # Creation des objets du jeu

        self.update() # On lance le jeu
        self.mainloop() # On lance Tk

    def buildGUI(self) : # Cette fonction initialise l'interface graphique
        self.ground = Canvas(self, width=self.size.width, height=self.size.height) # Creation du Canvas
        self.ground.config(cursor='cross') # On affiche un curseur en forme de croix
        self.ground.pack() # Affichage du Canvas

        self.photoRestart = PhotoImage(file='rc/images/refresh.gif') # Image de fond du bouton restart

        self.restartButton = Button(self, relief=FLAT, image=self.photoRestart, height=12, width=12, command=self.restart) # Creation du bouton restart
        self.restartButton.place(x=245, y=6) # On place le bouton

        self.photoVolume = PhotoImage(file='rc/images/volume_up.gif') # Image de fond du bouton volume

        self.volumeButton = Button(self, relief=FLAT, image=self.photoVolume, height=12, width=12, command=self.toggleVolume) # Creation du bouton volume
        self.volumeButton.place(x=220, y=6) # On place le bouton

        self.buildMenus() # On initialise les menus

        self.bind("<KeyPress>", self.keyDown) # On capte les evenenements de touche pressee
        self.bind("<KeyRelease>", self.keyUp) # On capte les evenenements de touche relachee
        self.ground.bind("<ButtonRelease-1>", self.click) # On capte les evenenements de touche de souris relachee

    def buildMenus(self) : # Cette fonction initialise les menus
        # ********** Creation des differents menus ********** #

        mainMenu = Menu(self)

        gameMenu = Menu(mainMenu, tearoff = 0)
        gameMenu.add_command(label = "Restart", accelerator="Ctrl+R", command=self.restart)
        gameMenu.add_command(label = "Scores", accelerator="Ctrl+S", command=self.showScores)
        gameMenu.add_separator()
        gameMenu.add_command(label = "Quit", accelerator="Ctrl+Q", command=self.destroy)

        self.bind_all("<Control-q>", lambda e : self.destroy())
        self.bind_all("<Control-r>", lambda e : self.restart())
        self.bind_all("<Control-s>", lambda e : self.showScores())

        aboutMenu = Menu(mainMenu, tearoff = 0)
        aboutMenu.add_command(label = "About this game...", command=self.showAboutDialog)

        mainMenu.add_cascade(label = "Game",menu = gameMenu)
        mainMenu.add_cascade(label = "About...", menu = aboutMenu)

        self.config(menu = mainMenu)

    def showScores(self) : # Cette fonction affiche les scores dans une boite de dialogue
        ScoresDialog(self.scoresManager)

    def showAboutDialog(self) : # Cette fonction affiche un message "A propos" dans une boite de dialogue
        AboutDialog()

    def initObjects(self) : # Cette fonction initialise tous les objets / variables du jeu
        self.pause = True # Cette variable determine si le jeu est en pause
        self.gameOver = False # Variable qui stocke l'etat du jeu (perdu / continue)
        self.points = 0 # Variable qui stocke le nombre de points du joueur
        self.stats = {'platforms_jump' : 0, 'monsters_jump' : 0, 'springs_jump': 0, 'trampolines_jump': 0, 'rockets' : 0, 'monsters_shot' : 0} # Cette variable contient les statistiques du joueur

        self.fps = CONSTS.SETTINGS_FPS # Frequence de rafraichissement du jeu (Frames Per Second)

        self.gravity = CONSTS.SETTINGS_GRAVITY # On initialise la gravite. Plus cette valeur est grande, plus le personnage tombe vite
        self.standardJumpVel = CONSTS.SETTINGS_STANDARD_JUMP_VEL # La velocite de base de saut du personnage

        self.random = CONSTS.SETTINGS_RANDOM # On initialise la variable qui determinera l'espacement des plateformes au cours du temps
        self.maxrandom = CONSTS.SETTINGS_MAX_RANDOM # On choisit une valeur maximale

        self.baseRandom = self.random # On conserve la valeur originale

        self.playerSize = Player().size # On recupere la taille par defaut du personnage en creant un objet anonyme
                                        # SANS lui indiquer le Canvas, sinon Player() sera dessine a la position 0,0 par defaut

        self.player = Player(self.ground) # On cree le personnage en lui indiquant la canvas
        self.player.move(Point(self.size.width / 2 - self.playerSize.width / 2, self.size.height / 3)) # On le place sur l'ecran
        self.player.setJump(True) # On active le saut directement (mais velocite verticale = 0 donc il tombe)

        self.floatingObjects = [] #  Cettte liste contient tous les objets flottants

        self.collisionmanager = CollisionManager(self.player) # On initialise le detecteur de collision en lui indiquant le personnage

        self.soundManager = SoundManager() # On initialise le gestionnaire de sons

        self.scoresManager = ScoresManager(CONSTS.FILE_SCORES) # On initialise le gestionnaire de scores

        self.background = [] # Cette liste contient tous les fonds parallax

        self.background.append(ParallaxBackground(self.ground, self.size, "rc/images/background.gif", .55)) # Creation d'un fond
        self.background.append(ParallaxBackground(self.ground, self.size, "rc/images/planets.gif", .65)) # Creation d'un autre fond

        self.createPlatforms() # On cree les plateformes
        self.scroll = 0 # Cette variable stocke la valeur actuelle de defilement - C'est aussi cette variable qui permet d'obtenir le nombre de points du joueur
        self.remainScroll = 0 # Cette variable stocke de combien on defile en "trop" par rapport a la hauteur des plateformes
        self.emptyPlaformCount = 0 # Cette variable stocke le nombre de plateformes vides

        self.displayInfos = OnScreenInfos(self.ground, self.size) # On place les infos à l'ecran
        self.displayInfos.setWelcomeTextVisibility(True) # On affiche le texte de bienvenue

        self.shotVect = Point(0, 0) # Vecteur de direction des projectiles

    def update(self) : # Cette fonction est appelee self.fps fois par seconde pour actualiser l'affichage
        # On ajuste le niveau d'aleatoire en fonction de l'avancement dans le jeu
        # Grace a cette fonctionnalite, les plateformes seront de plus en plus espacees pour augmenter la difficulte
        self.random = self.baseRandom + (self.scroll / 10e4) # Plus on monte plus les plateformes sont espacees
        if(self.random > self.maxrandom) : # Si on atteint une certaine valeur de seuil
            self.random = self.maxrandom # On en reste la, faut pas exagerer

        self.updateCollisions() # On actualise les collisions

        if not self.player.flying : # Si le personnage ne vole pas
            self.updateJump() # On actualise le saut du personnage
        else : # Sinon
            self.movePlayer(Point(self.player.inGamePos.x, self.player.inGamePos.y + self.player.flyingSpeed)) # On fait voler le personnage
            self.player.setFlyingFrameCount(self.player.flyingFramesCount - 1) # On reduit le temps de vol

        if self.player.proxyDrawFunc != self.player.defDraw : # Si le dessin du personnage passe par un proxy
            self.player.draw() # On l'actualise à chaque frame

        if self.player.flyingFramesCount == 0 : # Si le personnage a fini de voler
            if self.player.flyingOrigin == CONSTS.FLIGHT_ORIGIN_ROCKET : # Si le personnage etait dans une fusee
                self.player.removeProxyDraw() # On supprime le proxy
                self.player.fly(False, 0, 0, -1) # On le fait arreter de voler
                self.jump(self.standardJumpVel * 2) # Le personnage conserve une impulsion

        self.updateFloatingObjects() # On actualise les objets flottants

        self.updateShotVect() # On actualise le vecteur des projectiles

        self.removeOffScreenObjects() # On supprime les objets qui sont en dehors de l'ecran

        self.player.setOnTop() # On s'assure que le personnage soit bien au dessus du reste

        self.updateBullets() # On actualise les projectiles

        self.checkIfGameIsOver() # On verifie qu'on a pas perdu
        self.updateInfos() # On actualise les infos affichees a l'ecran

        if not self.gameOver and not self.pause : # Tant qu'on a pas perdu et que le jeu n'est pas en pause, il continue
            self.after(int(1000 / self.fps), self.update) # C'est reparti pour un tour

    def updateShotVect(self) : # Cette fonction calcule le vecteur qui dirige les projectiles en fonction de la position de la souris et du joueur
        x1 = self.player.pos.x + self.player.size.width / 2 # |--> On recupere les coordonees du personnage
        y1 = self.player.pos.y                              # |

        x2 = (self.winfo_pointerx() - self.winfo_rootx())   # |--> On recupere les coordonees de la souris
        y2 = (self.winfo_pointery() - self.winfo_rooty())   # |

        x = x2 - x1 # |--> On recupere les coordonees de la souris relatives au joueur
        y = y1 - y2 # |

        self.shotVect = Point(x, y) # On actualise le vecteur

    def updateBullets(self) : # Cette fonction actualise les projectiles
        for bullet in self.player.bullets : # Pour chaque projectiles
            bullet.translate(Point(bullet.vel * bullet.vect.x, -bullet.vel * bullet.vect.y)) # On le bouge de son propre vecteur

    def updateFloatingObjects(self) : # Cette fonction actualise les objets flottants
        for object in self.floatingObjects : # Pour chaque objet de la liste
            if object : # S'il n'est pas nul
                object.draw() # On l'actualise

    def updateCollisions(self) :
        if not self.player.alive: # Si le joueur est mort
            return # Il ne provoque plus aucune collision (en fait il va tomber tout en bas et puis Game Over)

        # ****** Plateformes ****** #
        # Fonctions de saut, tres important !
        # Le mecanisme de detection des collisions sur les plateformes doit-etre parfait pour assurer une cinematique globale correcte.
        if self.collisionmanager.playerFallOnObject(self.platforms) : # Si le personnage tombe sur une plateforme
            self.soundManager.playSound(CONSTS.SOUND_JUMP) # On lance le son correspondant
            self.jump(self.standardJumpVel) # On effectue un saut d'une certaine valeur
            self.player.jumpAnimation() # On anime le personnage
            self.stats['platforms_jump'] += 1 # On augmente le compte

        if not self.player.hittable : # Si le personnage de permet pas les collisions (ex.: il vole)
            return # On retourne immediatement

        # ******* Objets ****** #
        # Ici, on va faire la liste de tout les objets (attaches ou flottants)
        monsters    = [] # Cette liste stocke tout les monstres
        springs     = [] # Cette liste stocke tout les ressorts
        trampolines = [] # Cette liste stocke tout les trampolines
        rockets     = [] # Cette liste stocke toutes les fusees

        for line in self.platforms : # Pour chaque ligne de plateformes
            for platform in line : # Pour chaque plateforme de chaque ligne
                if platform : # Si il y a bien une plateforme a cet endroit
                    if platform.attachedObject : # Si cette plateforme a bien un objet attache
                        # On va lister chaque type d'objet avec isinstance()
                        if isinstance(platform.attachedObject, Monster) : # Si c'est un monstre
                            monsters.append(platform.attachedObject) # On l'ajoute a la liste
                        elif isinstance(platform.attachedObject, Spring) : # Si c'est un ressort
                            springs.append(platform.attachedObject) # On l'ajoute a la liste
                        elif isinstance(platform.attachedObject, Trampoline) : # Si c'est un ressort
                            trampolines.append(platform.attachedObject) # On l'ajoute a la liste
                        elif isinstance(platform.attachedObject, Rocket) : # Si c'est un ressort
                            rockets.append(platform.attachedObject) # On l'ajoute a la liste

        # => Monstres

        lowerMonsterHit = self.collisionmanager.getLowerObject(self.collisionmanager.detectCollision([monsters])) # On recupere le montre touche le plus bas
                                                                                                                  # Note: detectCollision() prend en parametres un tableau a 2 dimensions, d'ou ([monsters])

        if lowerMonsterHit : # Si le personnage a bien touche un monstre
            if self.player.velY > 0 : # Si le personnage monte (il arrive donc sous le monstre)
                self.soundManager.playSound(CONSTS.SOUND_MONSTER_DEAD) # On lance le son correspondant
                self.player.kill() # Il meurt, c'est triste mais c'est comme ca...
                self.player.setJump(True) # On le fait tomber dans le vide
            elif self.player.velY <= 0 : # Si il tombe (il arrive donc sur le monstre)
                self.player.jumpAnimation() # On anime le personnage
                self.soundManager.playSound(CONSTS.SOUND_MONSTER) # On lance le son correspondant
                lowerMonsterHit.detachFromParent() # PAF! Il ecrase le monstre. On detache donc le monstre en question
                self.floatingObjects.append(lowerMonsterHit) # Le monstre n'est plus attache a une plateforme, on l'ajoute donc a la liste des objets flottants (sinon le garbage-collector le supprimera)
                lowerMonsterHit.kill() # On lui dit qu'il est mort, alors il va tomber
                self.jump(self.standardJumpVel * lowerMonsterHit.velYCoef) # On effectue un saut d'une certaine valeur (plus haut que la normale)
                self.stats['monsters_jump'] += 1 # On augmente le compte

        # => Ressorts

        if self.collisionmanager.playerFallOnObject([springs]) : # Si le personnage tombe sur un ressort
            self.player.jumpAnimation() # On anime le personnage
            self.soundManager.playSound(CONSTS.SOUND_SPRING) # On lance le son correspondant
            self.player.setJump(True) # On dit qu'il saute
            self.jump(self.standardJumpVel * Spring().velYCoef) # On effectue un saut d'une certaine valeur
            self.stats['springs_jump'] += 1 # On augmente le compte

        # => Trampolines

        if self.collisionmanager.playerFallOnObject([trampolines]) : # Si le personnage tombe sur un ressort
            self.player.jumpAnimation() # On anime le personnage
            self.soundManager.playSound(CONSTS.SOUND_TRAMPOLINE) # On lance le son correspondant
            self.player.setJump(True) # On dit qu'il saute
            self.jump(self.standardJumpVel * Trampoline().velYCoef) # On effectue un saut d'une certaine valeur
            self.stats['trampolines_jump'] += 1 # On augmente le compte

        # => Fusees

        lowerRocketHit = self.collisionmanager.getLowerObject(self.collisionmanager.detectCollision([rockets])) # On recupere la fusee atteinte

        if lowerRocketHit and self.player.pos.y + self.player.size.height > lowerRocketHit.pos.y + lowerRocketHit.size.height / 2: # Si les coordonees sont correctes
            self.soundManager.playSound(CONSTS.SOUND_ROCKET) # On lance le son correspondant
            self.player.setProxyDraw(lowerRocketHit.initDrawPlayer, lowerRocketHit.drawPlayer, lowerRocketHit.removeDrawPlayer) # On met un proxy a la fonction de dessin du personnage
                                                                                                                                # C'est grace a ce macanisme que c'est une fusee qui est dessinee
            self.player.fly(True, 2.5 * self.fps, 30, CONSTS.FLIGHT_ORIGIN_ROCKET) # On fait voler le personnage
            lowerRocketHit.removeFromParent() # On detache la fusee de la plateforme
            self.stats["rockets"] += 1 # On augmente le compte

        # => Projectiles

        for bullet in self.player.bullets : # Pour chaque projectile
            manager = CollisionManager(bullet) # On cree un gestionnaire de collisions
            lowerMonsterShot = manager.getLowerObject(manager.detectCollision([monsters])) # On recupere le montre touche le plus bas

            if lowerMonsterShot : # S'il y a bien un monstre touche
                self.soundManager.playSound(CONSTS.SOUND_MONSTER_SHOT) # On lance le son correspondant
                lowerMonsterShot.detachFromParent() # Le monstre est tue. On detache donc le monstre en question
                self.floatingObjects.append(lowerMonsterShot) # Le monstre n'est plus attache a une plateforme, on l'ajoute donc a la liste des objets flottants (sinon le garbage-collector le supprimera)
                lowerMonsterShot.kill() # On lui dit qu'il est mort, alors il va tomber
                self.stats['monsters_shot'] += 1 # On augmente le compte
                self.points += CONSTS.BONUS_MONSTER_SHOT # Bonus de 100 pts


    def createPlatforms(self) : # Cette fonction genere les plateformes a l'initialisation du jeu
        pSize = Platform().size # On recupere la taille par defaut des plateformes en creant un objet anonyme
                                # SANS lui indiquer le Canvas, sinon Platform() sera dessinee a la position 0,0 par defaut

        self.platforms = [] # On cree le tableau contenant les plateformes

        for i in range(0, self.size.height // pSize.height) : # Pour chaque ligne de plateforme
            line = [] # On cree une nouvelle ligne de plateformes

            for j in range(0, self.size.width // pSize.width) : # Pour chaque colonne de plateforme
                if random.random() > self.random and i > 0 and not self.platforms[i - 1][j]: # On choisit aleatoirement si il y aura une plateforme
                    platform = Platform(self.ground) # On cree une nouvelle plateforme
                    platform.move(Point(pSize.width * j, (pSize.height * i))) # On la place correctement
                    line.append(platform) # On l'ajoute a la ligne
                else :
                    line.append(None) # Si aucune plateforme n'a ete generee, on ajoute "None" a la ligne

            self.platforms.append(line) # On ajoute la ligne entiere

    # Cette fonction fait defiler les plateformes D'UN VECTEUR VERTICAL ARBITRAIRE.
    # Encore une fois, cette fonction est tres importante car elle permet d'avancer dans le jeu.
    # Elle est utilisee conjointement avec la fonction movePlayer() pour permettre au personnage de se deplacer.
    def scrollPlatforms(self, vectY) :
        vectY = int(vectY) # On convertis en "int", au cas ou...

        self.scrollBackground(vectY) # On fait defiler les fonds parallax

        self.scroll += vectY # On incremente la valeur de defilement en fonction du vecteur vectY
        self.remainScroll += vectY # On incremente la variable en fonction du vecteur vectY

        pSize = Platform().size # On recupere la taille par defaut des plateformes en creant un objet anonyme
                                # SANS lui indiquer le Canvas, sinon Platform() sera dessinee a la position 0,0 par defaut

        pLineCount = self.remainScroll // pSize.height # On calcule combien il faut de nouvelles lignes
        pCount = self.size.width // pSize.width # On calcule combien il faut de plateformes

        # On fait défiler toutes les plateformes deja presentes
        for platformsLine in self.platforms : # Pour chaque ligne
            for platform in platformsLine : # Pour chaque plateforme dans la ligne
                if platform : # S'il y a bien une plateforme
                    platform.translate(Point(0, vectY)) # On la deplace de la valeur passee en parametres de la fonction

        # On cree les nouvelles plateformes
        if pLineCount > 0 : # S'il y a bien de nouvelles plateformes a ajouter
            self.remainScroll %= pSize.height # On calcul de combien on defile "de trop"

            for i in range(0, pLineCount) : # Pour chaque nouvelle ligne necessaire
                line = [] # On initialise une nouvelle ligne

                for j in range(0, pCount) : # Pour chaque plateforme dans la ligne
                    if (random.random() > self.random and not self.platforms[0][j]) or self.emptyPlaformCount >= pCount * 2 : # On choisit aleatoirement si il y aura une plateforme et on verifie qu'il n'y a pas de plateforme au dessous (pour ne pas les superposer)
                                                                                                                              # On s'assure aussi qu'il y a suffisament de plateformes pour que le joueur puisse sauter
                        c = Point(j * pSize.width, (pLineCount * i) - (i * pSize.height) + self.remainScroll) # On calcule la position de la plateforme
                        if self.checkSpace([i, j], c) : # On verifie qu'il y a bien l'espace pour la nouvelle plateforme
                            p = self.createPlatform() # On cree une nouvelle plateforme
                            self.setRandomObject(p) # On place un objet aleatoirement sur la plateforme
                            p.move(c) # On la place correctement
                            line.append(p) # On l'ajoute a la ligne
                            self.emptyPlaformCount = 0 # On reinitialise le compte de platefomres vides
                        else : # S'il n'y a pas d'espace
                            line.append(None) # Si aucune plateforme n'a ete generee, on ajoute "None" a la ligne
                    else :
                        line.append(None) # Si aucune plateforme n'a ete generee, on ajoute "None" a la ligne
                        self.emptyPlaformCount += 1 # On augmente le compte de platefomres vides

                self.platforms.insert(0, line) # On ajoute la ligne entiere

    def createPlatform(self) : # Cette fonction genere une plateforme en fonction de differents criteres
        if random.random() > CONSTS.OBJ_RND_AUTODESTRUCT and self.scroll > CONSTS.OBJ_SCROLL_AUTODESTRUCT : # Si on doit generer un plateforme qui s'auto-detruit
            return AutoDestructingPlatform(self.ground) # On la genere
        else : # Sinon
            return Platform(self.ground) # On genere une plateforme normale

    def checkSpace(self, index, coords) : # Cette fonction verifie que l'espace est suffisant pour ajouter une nouvelle plateforme
        for line in self.platforms : # Pour chaque ligne
            p = line[index[1]] # On recupere la plateforme au meme index horizontal que la plateforme a tester
            if p and p.attachedObject: # S'il y a bien une plateforme et qu'elle a un objet attache
                if p.attachedObject.pos.y - p.attachedObject.size.height < coords.y + Platform().size.height : # Si cet objet occupe deja l'espace
                    return False # On retourne "False"

        return True # On retourne "True"

    def removeOffScreenObjects(self) : # Cette fonction supprime les objets qui sont en dehors de l'ecran (trop en bas), pour des questions de performances
        # ****** Plateformes ****** #

        # Note: Un objet attache a une plateforme est supprime lorsque celle ci est supprimee

        pSize = Platform().size # On recupere la taille par defaut des plateformes en creant un objet anonyme
                                # SANS lui indiquer le Canvas, sinon Platform() sera dessinee a la position 0,0 par defaut

        for i, line in enumerate(self.platforms) : # Pour chaque ligne
            if (i * pSize.height) > self.size.height : # Si la position Y de la ligne est superieure a la taille verticale de la fenetre
                for platform in line : # Pour chaque plateforme dans cette ligne
                    if platform : # S'il y a bien une plateforme
                        platform.remove() # On supprime la plateforme (cette fonction supprime les graphismes du canvas, cela allege le jeu)
                del self.platforms[i] # On supprime la ligne tu tableau

        for i, line in enumerate(self.platforms) : # Pour chaque ligne
            for j, platform in enumerate(line) : # Pour chaque plateforme
                if platform : # S'il y a bien une plateforme
                    if platform.needsToBeRemoved : # Si elle doit-etre supprimee
                        self.soundManager.playSound(CONSTS.SOUND_AUTODESTRUCT) # On lance le son correspondant
                        platform.remove() # On la supprime
                        self.platforms[i][j] = None # On la supprime

        # ****** Objets flottants ****** #

        for i, object in enumerate(self.floatingObjects) : # Pour chaque ojet de la liste
            if object : # Si l'objet n'est pas nul
                if object.pos.y > self.size.height : # Si il est en dehors de l'ecran (trop bas)
                    object.remove() # On le supprime de l'affichage
                    del self.floatingObjects[i] # On le supprime de la liste

        # ****** Projectiles ****** #

        for i, bullet in enumerate(self.player.bullets) : # Pour chaque projectile
            if bullet.pos.y < 0 : # S'il atteint le haut de l'ecran
                bullet.remove() # On le supprime de l'affichage
                del self.player.bullets[i] # On le supprime de la liste

    def setRandomObject(self, platform) : # Cette fonction place un objet aleatoire sur la plateforme
        if random.random() > CONSTS.OBJ_RND_SPRING and self.scroll > CONSTS.OBJ_SCROLL_SPRING: # Si on depasse le seuil
            platform.setAttachedObject(Spring(self.ground), Point(5, 3)) # On place un ressort
            return # On sort de la fonction

        if random.random() > CONSTS.OBJ_RND_TRAMPOLINE and self.scroll > CONSTS.OBJ_SCROLL_TRAMPOLINE: # Si on depasse le seuil
            platform.setAttachedObject(Trampoline(self.ground), Point(3, 3)) # On place un trampoline
            return # On sort de la fonction

        if random.random() > CONSTS.OBJ_RND_MONSTER and self.scroll > CONSTS.OBJ_SCROLL_MONSTER: # Si on depasse le seuil
            platform.setAttachedObject(Monster(self.ground), Point(0, 3)) # On place un monstre
            return # On sort de la fonction

        if random.random() > CONSTS.OBJ_RND_ROCKET and self.scroll > CONSTS.OBJ_SCROLL_ROCKET: # Si on depasse le seuil
            platform.setAttachedObject(Rocket(self.ground), Point(0, 2)) # On place une fusee
            return # On sort de la fonction

    def scrollBackground(self, vectY) : # Cette fonction fait defiler les fonds parallax
        for bg in self.background : # Pour chaque fond
            bg.scroll(vectY) # On le fait defiler

    def checkIfGameIsOver(self) : # Cette fonction verifie qu'on a pas perdu
        if self.player.pos.y - self.player.size.height >= self.size.height - self.playerSize.height : # Si le personnage a atteint le bas de l'ecran (il est tombe trop bas)
            self.soundManager.playSound(CONSTS.SOUND_FALL) # On lance le son correspondant
            self.player.setJump(False) # Deja il arrete de tomber
            self.gameOver = True # On modifie l'etat du jeu

        if self.gameOver : # Si une autre fonction a deja stopee le jeu
            self.gameOverCallback() # On notifie que le jeu est fini

    def keyDown(self, event) : # Cette fonction est appelee a chaque touche pressee
        if not self.player.alive or self.gameOver : # Si le personnage est mort, il ne repond plus aux commandes
            return # Alors la fonction retourne directement

        if event.keysym == "space" : # Si on presse la touche "espace"
            self.displayInfos.setWelcomeTextVisibility(False) # On masque le texte de bienvenue
            self.displayInfos.setPause(self.pause) # On cache l'indicateur de pause
            self.pause = not self.pause # On inverse la variable self.pause
            self.update() # On update car quand le jeu est en pause la fonction update n'est plus appelee

        # Note: en pause, la seule touche qui peut declancher des actions est la touche espace

        if self.pause : # Si le jeu est en pause, il ne repond plus aux commandes
            return # Alors la fonction retourne directement

        if event.keysym == "Right" : # Si c'est la touche droite
            if self.player.pos.x > self.size.width : # Si le personnage est trop a droite
                self.player.translate(Point(-self.player.pos.x, 0)) # On le replace à gauche
            else : # Sinon
                self.player.translate(Point(10, 0)) # On le deplace de 10px vers la droite
        elif event.keysym == "Left" : # Si c'est la touche gauche
            if self.player.pos.x < -self.player.size.width : # Si le personnage est trop à gauche
                self.player.translate(Point(self.size.width, 0)) # On le replace a droite
            else : # Sinon
                self.player.translate(Point(-10, 0)) # On le deplace de 10px vers la gauche
        elif event.keysym == "Up" : # Si c'est la touche haut
            #self.jump(self.standardJumpVel * 2) # On fait sauter le personnage (uniquement utile pour le debogage)
            pass # Pas de cheat, S.V.P.
        elif event.keysym == "Down" : # Si c'est la touche bas
            #self.player.velY = 0 # On fait tomber le personnage (uniquement utile pour le debogage)
            pass

    def keyUp(self, event) : # Cette fonction est appelee a chaque touche relachee
        pass # Bah en fait elle ne sert a rien ^^

    def click(self, event) :
        if not self.player.alive or self.gameOver or self.pause: # Si le personnage est mort ou que le jeu est en pause
            return # Alors la fonction retourne directement

        self.triggerShot() # On declanche un coup de feu

    # Cette fonction est utilisee pour bouger le personnage dans l'espace du jeu,
    # elle traduit ensuite cette position en position absolue a l'ecran et declanche eventuellement un defilement des plateformes.
    # C'est (en partie) sur cette fonction que repose le fonctionnement du jeu. C'est pourquoi son fonctionnement doit-etre irreprochable.
    def movePlayer(self, pos) :
        yTrans = pos.y - self.player.inGamePos.y # On calcule la translation correspondant a la position demandee

        if self.player.inGamePos.y < pos.y : # Si le personnage va vers le haut
            if self.player.pos.y - yTrans > self.size.height / 2 : # Et qu'il n'a pas atteint la moitie verticale de la fenetre
                self.player.translate(Point(pos.x - self.player.inGamePos.x, -yTrans)) # On le bouge a l'ecran
                self.scroll += yTrans # On augmente la valeur de defilement. /!\ Ceci ne fait pas defiler les plateformes, c'est utile pour le compte des points
            else : # Si le personnage atteint la moitie superieure de la fenetre
                self.scrollPlatforms(yTrans) # Alors le personnage reste au milieu et ce sont les plateformes qui defilent
        elif self.player.inGamePos.y > pos.y : # Si le personnage va vers le bas
            self.player.translate(Point(pos.x - self.player.inGamePos.x, -yTrans)) # Dans ce cas, on deplace le personnage sans se poser de questions
            self.scroll += yTrans # On diminue la valeur de defilement. /!\ Ceci ne fait pas defiler les plateformes, c'est utile pour le compte des points

        self.player.inGamePos = pos # On actualise la position du personnage dans l'espace du jeu

    def jump(self, velY) : # Cette fonction fait sauter le personnage
        self.player.setVelY(velY) # On modifie sa velocite verticale (velY > 0 , alors il monte)
        self.player.setJump(True) # On notifie u'il saute

    def updateJump(self) : # Cette fonction actualise le saut du personnage (cela signifie aussi que cette fonction peu le faire tomber si self.player.velY < 0)
        if self.player.jump : # Si le personnage est bien en train de sauter
            self.player.velY -= self.gravity # On reduit sa velocite verticale en fonction de la gravite
            # Note: -> Si self.player.velY < 0 : le personnage tombe
            #       -> Si self.player.velY > 0 : le personnage monte
            #       -> Si self.player.velY = 0 : le personnage reste statique
            self.movePlayer(Point(self.player.inGamePos.x, self.player.inGamePos.y + self.player.velY)) # On deplace le personnage DANS L'ESPACE DU JEU, ET NON PAS A L'ECRAN DIRECTEMENT

    def triggerShot(self) : # Cette fonction declanche un coup de feu
        if self.player.flyingOrigin == -1 and (self.winfo_pointery() - self.winfo_rooty()) < self.player.pos.y: # Si le personnage ne vole pas et que la souris et au dessus du personnage
            self.soundManager.playSound(CONSTS.SOUND_SHOT) # On lance le son correspondant
            self.player.shot(self.shotVect) # On fait tirer le personnage en fonction du vecteur

    def updateInfos(self) : # Cette fonction s'occupe d'actualiser les infos (nombre de points, ect...), rien de bien complique
        if self.scroll > self.points : # Si le personnage a encore monte depuis le dernier appel a la fonction
            self.points = int(self.scroll) # On actualise le nombre de points (que l'on convertis en entiers, c'est mieux)

        self.displayInfos.setPoints(self.points) # On affiche les points a l'ecran
        self.displayInfos.setOnTop() # On place ces infos par dessus TOUT le reste (z-index)

    def gameOverCallback(self) : # Cette fonction est une fonction de rappel (callback en anglais) appelee quand on a perdu
        self.displayInfos.gameOver(self.points, self.stats) # On affiche un message de fin a l'ecran
        self.scoresManager.addScore(self.points, datetime.datetime.now()) # On sauvegarde les scores
        #messagebox.showinfo("Game over !", "You're a looser ! :P\nYou got {} points. Here are your stats :\n- {} jumps on platforms\n- {} jumps on monsters\n- {} jumps on springs".format(self.points, self.stats['platforms_jump'], self.stats['monsters_jump'], self.stats['springs_jump'])) # On affiche une boite de dialogue (temporaire uniquement)

    def restart(self) : # Cette fonction est appelee quand le bouton restart est presse
        self.soundManager.stopAll() # On coupe tous les sons

        if self.soundManager.mute : # Si le son est en mode muet
            self.toggleVolume() # On le remet normal

        self.initObjects() # On reinitialise le jeu

    def toggleVolume(self) : # Cette fonction permet d'activer / desactiver le son
        self.soundManager.setMute(not self.soundManager.mute); # On bascule l'audio sur muet ou son

        if self.soundManager.mute : # Si c'est en muet
            self.photoVolume = PhotoImage(file='rc/images/volume_off.gif') # Image de fond du bouton volume
        else : # Sinon
            self.photoVolume = PhotoImage(file='rc/images/volume_up.gif') # Image de fond du bouton volume

        self.volumeButton.configure(image = self.photoVolume) # On change l'image du bouton

# On lance le jeu une bonne fois pour toutes
Game(Size(300, 500)) # On cree l'objet jeu d'une taille de 300x500 px, et c'est parti !
