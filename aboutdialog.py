""" Cette classe est une boite de dialogue qui affiche un message 'A propos' """

from tkinter import * # On importe les modules Tk necessaires

class AboutDialog(Toplevel) :
    def __init__(self) :
        Toplevel.__init__(self)

        self.resizable(width=False, height=False)
        self.title("More")
        self.geometry("400x300")

        self.text = Text(self, relief=FLAT)
        self.text.insert(END, "This game was made by ANDRE Marie and BOST Grégoire in Python with the Tkinter library.\n\nSpace Jumper was inspired by \"Doodle Jump\".\n\nThe rules are simple: just jump as long as you can on the platforms when avoiding monsters ! If you fall... You lose !\n\nThis project was made as part of the bachelor's diploma. This program does not claim to be a \"professional-grade\" game but a school exercise.")
        self.text.config(state=DISABLED)
        self.text.config(cursor='arrow')
        self.text.pack()
