import tkinter as tk
from tkinter import ttk
import json
import os
from tkinter import messagebox


class BattleWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fenêtre de Bataille")
        self.geometry("800x600")

        # Charger les divisions sauvegardées
        self.divisions = self.load_divisions()

        # Cadre pour les paramètres de la bataille
        frame_params = tk.Frame(self)
        frame_params.pack(fill=tk.X, pady=10)

        tk.Label(frame_params, text="Météo").grid(row=0, column=0, padx=5)
        self.weather = tk.StringVar()
        tk.Entry(frame_params, textvariable=self.weather).grid(row=0, column=1, padx=5)

        tk.Label(frame_params, text="Terrain").grid(row=0, column=2, padx=5)
        self.terrain = tk.StringVar()
        tk.Entry(frame_params, textvariable=self.terrain).grid(row=0, column=3, padx=5)

        tk.Label(frame_params, text="Leader Camp A").grid(row=1, column=0, padx=5)
        self.leader_a = tk.StringVar()
        tk.Entry(frame_params, textvariable=self.leader_a).grid(row=1, column=1, padx=5)

        tk.Label(frame_params, text="Leader Camp B").grid(row=1, column=2, padx=5)
        self.leader_b = tk.StringVar()
        tk.Entry(frame_params, textvariable=self.leader_b).grid(row=1, column=3, padx=5)

        # Cadre pour les camps
        frame_battle = tk.Frame(self)
        frame_battle.pack(fill=tk.BOTH, expand=True, pady=10)

        # Camp A
        frame_camp_a = tk.Frame(frame_battle)
        frame_camp_a.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(frame_camp_a, text="Camp A").pack()
        self.camp_a_divisions = tk.Listbox(frame_camp_a)
        self.camp_a_divisions.pack(fill=tk.BOTH, expand=True, pady=5)

        self.add_division_a = tk.StringVar()
        dropdown_a = ttk.Combobox(frame_camp_a, textvariable=self.add_division_a, values=self.get_division_names())
        dropdown_a.pack(pady=5)
        tk.Button(frame_camp_a, text="Ajouter Division",
                  command=lambda: self.add_division(self.camp_a_divisions, self.add_division_a)).pack()

        # Camp B
        frame_camp_b = tk.Frame(frame_battle)
        frame_camp_b.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(frame_camp_b, text="Camp B").pack()
        self.camp_b_divisions = tk.Listbox(frame_camp_b)
        self.camp_b_divisions.pack(fill=tk.BOTH, expand=True, pady=5)

        self.add_division_b = tk.StringVar()
        dropdown_b = ttk.Combobox(frame_camp_b, textvariable=self.add_division_b, values=self.get_division_names())
        dropdown_b.pack(pady=5)
        tk.Button(frame_camp_b, text="Ajouter Division",
                  command=lambda: self.add_division(self.camp_b_divisions, self.add_division_b)).pack()

        # Bouton pour lancer un round de la bataille
        tk.Button(self, text="Lancer un Round", command=self.run_battle_round).pack(pady=10)

        # Zone de logs pour les résultats
        self.log_text = tk.Text(self, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_divisions(self):
        if os.path.exists("divisions.json"):
            with open("divisions.json", "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def get_division_names(self):
        return [division["Nom de la division"] for division in self.divisions]

    def add_division(self, listbox, selected_division_var):
        selected_name = selected_division_var.get()
        if selected_name and selected_name not in listbox.get(0, tk.END):
            listbox.insert(tk.END, selected_name)

    def run_battle_round(self):
        # Ici tu ajoutes le code pour lancer le calcul de la bataille
        log_entry = "Résultats du round de bataille...\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)


app = BattleWindow()
app.mainloop()
