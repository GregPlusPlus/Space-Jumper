""" Cette classe permet de detecter les collisions entre les objets du jeu """

from graphicgamecomponent import * # On importe la classe GraphicGameComponent (c'est un composant du jeu)
from player import * # On importe la classe Player (c'est un composant du jeu)

class CollisionManager :
    def __init__(self, testedObject) : # Constructeur prenant en parametres l'objet a tester
        self.testedObject = testedObject # On stocke cet objet

    def detectCollision(self, objects) : # Cette fonction detecte les collisions entre l'objet et une liste d'objets a deux dimensions
        result = [] # Ce tableau contiendra la liste des objets entres en collision

        for line in objects : # Pour chaque ligne du tableau
            for object in line : # Pour chaque objet de chaque ligne
                if object : # S'il y a bien un objet a cet index
                    # On teste chaque objet du tableau avec l'objet a tester, c'est long mais ca marche ! o.O
                    if self.testedObject.pos.x < object.pos.x + object.size.width and self.testedObject.pos.x + self.testedObject.size.width > object.pos.x and self.testedObject.pos.y < object.pos.y + object.size.height and self.testedObject.pos.y + self.testedObject.size.height > object.pos.y :
                        object.hit(self.testedObject) # On appelle la fonction hit() pour indiquer a l'objet qu'il a ete percute
                        result.append(object) # On ajoute l'objet a la liste

        return result # On retourne la liste des objets entres en collision

    def getLowerObject(self, objects) : # Cette fonction recupere l'objet le blus bas (qui a l'ordonnee la plus grande) parmi une liste
        # Note: cette fonction reviens exactement faire a une recherche de maximum dans une liste

        if len(objects) == 0 : # Si la liste est vide
            return None # Bah il n'y a aucun objet a retourner, donc on retourne "None"

        lower = objects[0] # On initialise le premier objet

        for current in objects : # Pour chaque objet dans la liste
            if current.pos.y >= lower.pos.y : # Si on a trouve un autre objet avec une ordonnee plus grande
                lower = current # On remplace l'objet par le nouveau

        return lower # On retourne l'objet le plus en bas

    def playerFallOnObject(self, objects) : # Cette fonction detecte si le personnage tombe sur un objet
        if not isinstance(self.testedObject, Player) : # On teste si l'objet a tester est de type player
            return None # Sinon on retourne rien

        lowerObjectHit = self.getLowerObject(self.detectCollision(objects)) # On recupere l'objet touche le plus bas

        if lowerObjectHit : # S'il y a bien un objet
            if self.testedObject.pos.y + self.testedObject.size.height < lowerObjectHit.pos.y + lowerObjectHit.size.height : # On teste que le bas du personnage est bien au dessus de l'objet touche
                if self.testedObject.velY < 0 : # Si le personnage tombe
                    lowerObjectHit.fallOn(self.testedObject)
                    return lowerObjectHit # On retorne l'objet

        return None # S'il n'y a pas d'objet bah on retourne rien
