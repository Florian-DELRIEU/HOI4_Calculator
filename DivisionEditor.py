import tkinter as tk
from tkinter import ttk


class DivisionEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Éditeur de Division")
        self.geometry("600x400")

        # Définition des statistiques de la division
        self.stats = {
            "Nom de la division": tk.StringVar(),
            "PV": tk.IntVar(),
            "Organisation": tk.IntVar(),
            "Soft Attack": tk.IntVar(),
            "Hard Attack": tk.IntVar(),
            "Defense": tk.IntVar(),
            "Attaque": tk.IntVar(),
            "Piercing": tk.IntVar(),
            "Armor": tk.IntVar(),
            "Hardness": tk.DoubleVar(),
            "Entrenchment": tk.DoubleVar(),
            "Width": tk.IntVar()
        }

        # Création des champs de saisie
        row = 0
        col = 0
        for i, (stat, var) in enumerate(self.stats.items()):
            if i == 0:  # Nom de la division sur une ligne à part
                tk.Label(self, text=stat).grid(row=row, columnspan=2, pady=5, sticky=tk.W)
                tk.Entry(self, textvariable=var).grid(row=row + 1, columnspan=2, pady=5)
                row += 2
                continue

            tk.Label(self, text=stat).grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)
            tk.Entry(self, textvariable=var).grid(row=row, column=col + 1, padx=5, pady=5)

            if col == 0:
                col = 2
            else:
                col = 0
                row += 1

        # Bouton de sauvegarde
        tk.Button(self, text="Sauvegarder", command=self.save_division).grid(row=row + 1, columnspan=4, pady=10)

    def save_division(self):
        division_data = {stat: var.get() for stat, var in self.stats.items()}
        print("Division sauvegardée:", division_data)
        # Code pour sauvegarder les données, par exemple dans un fichier ou une base de données


app = DivisionEditor()
app.mainloop()
