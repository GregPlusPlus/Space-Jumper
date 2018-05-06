""" Cette classe est le gestionnaire de scores """

from tkinter import messagebox # On importe le module messagebox

class ScoresManager :
    def __init__(self, fileName): # Constructeur qui prend en parametre le chemin du fichier
        self.fileName = fileName # On stocke le chemin

    def addScore(self, points, date) : # Cette fonction ajoute un score au fichier
        try : # On essaie d'ouvrir le fichier
            file = open(self.fileName, "a") # On ouvre le fichier
        except IOError :
            messagebox.showinfo("File error", "Unable to open the file '{}'".format(self.fileName)) # Si on a echoue
            return # On retourne immediatement

        file.write("{}|{}\n".format(points, date)) # On ecrit dans le fichier

    def loadScores(self) : # Cette fonction recupere les scores depuis un fichier et les place dans une liste
        try : # On essaie d'ouvrir le fichier
            file = open(self.fileName, "r") # On ouvre le fichier
        except IOError : # Si on a echoue
            messagebox.showinfo("File error", "Unable to open the file '{}'".format(self.fileName)) # On affiche une boite de dialogue
            return [] # On retourne immediatement

        scores = [] # On cree un tableau qui stocke les scores

        with file as fp: # On recupere le contenu du fichier
            for line in fp: # On recupere chaque ligne
                scoreLine = line.replace('\n', '').split('|') # On formatte

                if len(scoreLine) < 2 : # Si on a trouve moins de deux chaines dans la ligne on passe au suivant
                    continue # On passe

                scores.append([scoreLine[0], scoreLine[1].split('.')[0].replace('-', '/')]) # On ajoute le score a la liste

        return scores # On retourne les scores

    def clearFile(self) : # Cette fonction vide la liste de scores
        try : # On essaie d'ouvrir le fichier
            open(self.fileName, "w").close() # On ouvre le fichier en ecriture seule, puis on le ferme. Cela a pour effet de le vider.
        except IOError : # Si on a echoue
            messagebox.showinfo("File error", "Unable to open the file '{}'".format(self.fileName)) # On affiche une boite de dialogue
            return False # On retourne faux
        return True # On retourne vrai
