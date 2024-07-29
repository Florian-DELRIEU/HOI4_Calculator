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

        # Charger les divisions existantes pour le menu déroulant
        self.divisions = self.load_divisions()
        self.division_names = [division["Nom de la division"] for division in self.divisions]

        # Menu déroulant pour sélectionner une division
        self.selected_division = tk.StringVar()
        self.selected_division.set("Sélectionner une division")
        self.dropdown = ttk.Combobox(self, textvariable=self.selected_division, values=self.division_names)
        self.dropdown.pack(pady=10)
        self.dropdown.bind("<<ComboboxSelected>>", self.load_division)

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
            if division["Nom de la division"] == selected_name:
                for stat, var in self.stats.items():
                    var.set(division[stat])
                break

    def save_division(self):
        division_data = {stat: var.get() for stat, var in self.stats.items()}
        division_data["Nom de la division"] = self.stats["Nom de la division"].get()

        # Vérifier si une division avec le même nom existe déjà
        for division in self.divisions:
            if division["Nom de la division"] == division_data["Nom de la division"]:
                messagebox.showerror("Erreur", "Une division avec ce nom existe déjà.")
                return

        # Ajouter la nouvelle division
        self.divisions.append(division_data)

        # Sauvegarder toutes les divisions dans le fichier JSON
        with open("divisions.json", "w") as file:
            json.dump(self.divisions, file, indent=4)

        # Mettre à jour le menu déroulant
        self.division_names.append(division_data["Nom de la division"])
        self.selected_division.set("Sélectionner une division")
        self.selected_division.set("")
        self.selected_division.set("Sélectionner une division")
        self.dropdown['values'] = self.division_names

        print("Division sauvegardée:", division_data)


app = DivisionEditor()
app.mainloop()
