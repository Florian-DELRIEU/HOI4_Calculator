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
        self.dropdown = None

        # Définition des statistiques de la division
        self.stats = {
            "Nom de Template": tk.StringVar(),
            "PV": tk.DoubleVar(),
            "Organisation": tk.DoubleVar(),
            "Soft Attack": tk.DoubleVar(),
            "Hard Attack": tk.DoubleVar(),
            "Defense": tk.DoubleVar(),
            "Attaque": tk.DoubleVar(),
            "Piercing": tk.DoubleVar(),
            "Armor": tk.DoubleVar(),
            "Hardness": tk.DoubleVar(),
            "Width": tk.IntVar()
        }

        # Charger les divisions existantes pour le menu déroulant
        self.divisions = self.load_divisions()
        self.division_templates = [division["Nom de Template"] for division in self.divisions]

        # Menu déroulant pour sélectionner une division
        self.selected_division = tk.StringVar()
        self.selected_division.set("Sélectionner une template")
        self.dropdown = ttk.Combobox(self, textvariable=self.selected_division, values=self.division_templates)
        self.dropdown.pack(pady=10)
        self.dropdown.bind("<<ComboboxSelected>>", self.load_division)

        # Conteneur pour le Nom de Template
        frame_name = tk.Frame(self)
        frame_name.pack(fill=tk.X, pady=10)

        tk.Label(frame_name, text="Nom de Template").pack(side=tk.LEFT, padx=10)
        tk.Entry(frame_name, textvariable=self.stats["Nom de Template"]).pack(side=tk.LEFT, fill=tk.X, expand=True,
                                                                                 padx=10)

        # Conteneur pour les autres statistiques
        frame_stats = tk.Frame(self)
        frame_stats.pack(fill=tk.BOTH, expand=True)

        # Création des champs de saisie
        row = 0
        col = 0
        for i, (stat, var) in enumerate(self.stats.items()):
            if stat != "Nom de Template":
                tk.Label(frame_stats, text=stat).grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)
                tk.Entry(frame_stats, textvariable=var).grid(row=row, column=col + 1, padx=5, pady=5)

                if col == 0:
                    col = 2
                else:
                    col = 0
                    row += 1

        # Bouton de sauvegarde
        tk.Button(self, text="Sauvegarder", command=self.save_division).pack(pady=10)

    def load_divisions(self):
        if os.path.exists("divisions.json"):
            with open("divisions.json", "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def load_division(self, event):
        selected_name = self.selected_division.get()
        for division in self.divisions:
            if division["Nom de Template"] == selected_name:
                for stat, var in self.stats.items():
                    var.set(division[stat])
                break

    def save_division(self):
        division_data = {stat: var.get() for stat, var in self.stats.items()}
        division_data["Nom de Template"] = self.stats["Nom de Template"].get()

        # Vérifier si une division avec le même nom existe déjà
        for i, division in enumerate(self.divisions):
            if division["Nom de Template"] == division_data["Nom de Template"]:
                self.divisions[i] = division_data
                break
        else:
            # Ajouter la nouvelle division si elle n'existe pas déjà
            self.divisions.append(division_data)
            self.division_templates.append(division_data["Nom de Template"])

        # Sauvegarder toutes les divisions dans le fichier JSON
        with open("divisions.json", "w") as file:
            json.dump(self.divisions, file, indent=4)

        # Mettre à jour le menu déroulant
        self.selected_division.set("Sélectionner une division")
        self.dropdown['values'] = self.division_templates

        print("Division sauvegardée:", division_data)


app = DivisionEditor()
app.mainloop()
