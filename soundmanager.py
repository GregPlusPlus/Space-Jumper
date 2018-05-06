""" Cette classe permet de jouer des sons dans le jeu """

import winsound # On import le module winsound

from gameconsts import * # On importe la classe CONSTS (c'est un composant du jeu)

class SoundManager :
    def __init__(self, mute = False) : # Constructeur, peut prendre en parametre le mode muet
        self.mute = mute # Cette variable stocke le mode (muet / son)

    def playSound(self, path) : # Cette fonction joue un son
        if not self.mute : # Si ce n'est pas le mode muet
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC) # On joue le son

    def stopAll(self) : # Cette fonction arrete tous les sons
        winsound.PlaySound(None, winsound.SND_PURGE) # On arrete tous les sons

    def setMute(self, mute) : # Cette fonction permet de mettre les sons en muet
        if mute : # Si on demande en muet
            self.stopAll() # On arrete tous les sons

        self.mute = mute # On actualise la variable
