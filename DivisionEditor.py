import tkinter as tk
from tkinter import ttk
import json
import os
from tkinter import messagebox


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

        # Conteneur pour le nom de la division
        frame_name = tk.Frame(self)
        frame_name.pack(fill=tk.X, pady=10)

        tk.Label(frame_name, text="Nom de la division").pack(side=tk.LEFT, padx=10)
        tk.Entry(frame_name, textvariable=self.stats["Nom de la division"]).pack(side=tk.LEFT, fill=tk.X, expand=True,
                                                                                 padx=10)

        # Conteneur pour les autres statistiques
        frame_stats = tk.Frame(self)
        frame_stats.pack(fill=tk.BOTH, expand=True)

        # Création des champs de saisie
        row = 0
        col = 0
        for i, (stat, var) in enumerate(self.stats.items()):
            if stat != "Nom de la division":
                tk.Label(frame_stats, text=stat).grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)
                tk.Entry(frame_stats, textvariable=var).grid(row=row, column=col + 1, padx=5, pady=5)

                if col == 0:
                    col = 2
                else:
                    col = 0
                    row += 1

        # Bouton de sauvegarde
        tk.Button(self, text="Sauvegarder", command=self.save_division).pack(pady=10)

    def save_division(self):
        division_data = {stat: var.get() for stat, var in self.stats.items()}
        division_data["Nom de la division"] = self.stats["Nom de la division"].get()

        # Charger les divisions existantes ou créer une nouvelle liste
        if os.path.exists("divisions.json"):
            with open("divisions.json", "r") as file:
                try:
                    divisions = json.load(file)
                except json.JSONDecodeError:
                    divisions = []
        else:
            divisions = []

        # Vérifier si une division avec le même nom existe déjà
        for division in divisions:
            if division["Nom de la division"] == division_data["Nom de la division"]:
                messagebox.showerror("Erreur", "Une division avec ce nom existe déjà.")
                return

        # Ajouter la nouvelle division
        divisions.append(division_data)

        # Sauvegarder toutes les divisions dans le fichier JSON
        with open("divisions.json", "w") as file:
            json.dump(divisions, file, indent=4)

        print("Division sauvegardée:", division_data)


app = DivisionEditor()
app.mainloop()
