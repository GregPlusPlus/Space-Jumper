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

""" Cette classe est une boite de dialogue qui affiche un message 'A propos' """

from tkinter import * # On importe les modules Tk necessaires

class AboutDialog(Toplevel) :
    def __init__(self) :
        Toplevel.__init__(self)

        self.resizable(width=False, height=False)
        self.title("More")
        self.geometry("400x400")

        self.text = Text(self, relief=FLAT)
        self.text.insert(END, "This game was made by ANDRE Marie and BOST Grégoire in Python with the Tkinter library.\n\nSpace Jumper was inspired by \"Doodle Jump\".\n\nThe rules are simple: just jump as long as you can on the platforms when avoiding monsters ! If you fall... You lose !\n\nThis project was made as part of the bachelor's diploma. This program does not claim to be a \"professional-grade\" game but a school exercise.\n\nA version of this project is hosted here: <https://github.com/GregPlusPlus/Space-Jumper> and is available under the GNU LESSER GENERAL PUBLIC LICENSE.\n\n==================================\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n")
        self.text.config(state=DISABLED)
        self.text.config(cursor='arrow')
        self.text.pack()
