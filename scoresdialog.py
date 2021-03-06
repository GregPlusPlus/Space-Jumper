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

""" Cette classe est une boite de dialogue qui affiche les scores """

from tkinter import * # On importe les modules Tk necessaires

class ScoresDialog(Toplevel) :
    def __init__(self, manager) :
        Toplevel.__init__(self)

        self.scoresManager = manager

        self.resizable(width=False, height=False)
        self.title("Your scores")
        self.geometry("270x350")

        Label(self, text = "Scores : ").pack()

        self.frame = Frame(self)
        self.frame.pack()

        self.scoresList = Listbox(self.frame, width = 30, height = 14)
        self.scoresList.pack(side="left", fill="y")

        self.scrollbar = Scrollbar(self.frame, orient="vertical")
        self.scrollbar.config(command=self.scoresList.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scoresList.config(yscrollcommand=self.scrollbar.set)

        self.buttonClear = Button(self, text="Clear all", command=lambda : self.clearScores())
        self.buttonClear.pack()

        scores = self.scoresManager.loadScores()

        for score in scores :
            self.scoresList.insert(END, "{} ► {}".format(score[1], score[0]))

    def clearScores(self) :
        if messagebox.askquestion("Clear all", "Do you really want to clear all scores ?", icon='warning') != 'yes':
            return

        if self.scoresManager.clearFile() :
            self.scoresList.delete(0,END)
