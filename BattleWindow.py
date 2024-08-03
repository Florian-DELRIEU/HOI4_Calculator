import tkinter as tk
from tkinter import ttk
import json
import os
from Class import Division, Camp
from tkinter import messagebox

class BattleWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fenêtre de Bataille")
        self.geometry("800x600")

        # Initialiser les camps
        self.camp_a = Camp()
        self.camp_b = Camp()

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
        self.camp_a_divisions_frame = tk.Frame(frame_camp_a)
        self.camp_a_divisions_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Button(frame_camp_a, text="Ajouter Division", command=lambda: self.open_division_selection(self.camp_a, self.camp_a_divisions_frame)).pack()

        # Camp B
        frame_camp_b = tk.Frame(frame_battle)
        frame_camp_b.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(frame_camp_b, text="Camp B").pack()
        self.camp_b_divisions_frame = tk.Frame(frame_camp_b)
        self.camp_b_divisions_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Button(frame_camp_b, text="Ajouter Division", command=lambda: self.open_division_selection(self.camp_b, self.camp_b_divisions_frame)).pack()

        # Bouton pour lancer un round de la bataille
        tk.Button(self, text="Lancer un Round", command=self.run_battle_round).pack(pady=10)
        tk.Button(self, text="Sauvegarder Bataille", command=self.save_battle_data).pack(pady=10)

        # Zone de logs pour les résultats
        self.log_text = tk.Text(self, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_divisions(self):
        """
           Charge les divisions sauvegardées à partir d'un fichier JSON.
           Cette méthode vérifie l'existence du fichier "divisions.json" et tente de charger les données JSON à partir de ce fichier.
           Les données sont ensuite converties en instances de la classe Division.
           Retour:
               List[Division]: Une liste d'instances de la classe Division représentant les divisions sauvegardées.
           """
        if os.path.exists("divisions.json"):
            with open("divisions.json", "r") as file:
                try:
                    data = json.load(file)
                    return [Division.load(division) for division in data]
                except json.JSONDecodeError:
                    return []
        return []

    def get_division_names(self):
        """
           Récupère les noms de toutes les divisions sauvegardées.
           Cette méthode parcourt la liste des divisions chargées et extrait le nom de chaque division.
           Retour:
               List[str]: Une liste contenant les noms de toutes les divisions sauvegardées.
           """
        return [division.template for division in self.divisions]

    def add_division(self, frame, selected_division_var):
        """
           Ajoute une division au camp spécifié et affiche ses statistiques de manière compacte.

           Cette méthode recherche la division correspondant au nom sélectionné, crée un cadre pour la division,
           et affiche ses statistiques sous forme abrégée en colonnes, avec des barres de progression pour les PV et l'organisation.

           Args:
               frame (tk.Frame): Le cadre dans lequel ajouter la division (camp A ou camp B).
               selected_name (str): Le Nom de Template sélectionnée à ajouter.
           """
        if not (selected_name := selected_division_var.get()):
            return
        for division in self.divisions:
            if division.template == selected_name:
                if frame == self.camp_a_divisions_frame: self.camp_a.add_division(division)
                if frame == self.camp_b_divisions_frame: self.camp_b.add_division(division)
                frame_division = tk.Frame(frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
                frame_division.pack(fill=tk.X, pady=2)

                stats_frame = tk.Frame(frame_division)
                stats_frame.pack(fill=tk.X)

                stats = [division.pv,division.organisation,division.soft_attack,division.hard_attack,division.defense,
                division.attaque,division.piercing,division.armor,division.hardness,division.width]
                abbr_stats = ["PV", "Org", "SA", "HA", "Def", "Atk", "Prc", "Arm", "Hard", "Wdth"]

                for i, stat in enumerate(stats):
                    row = i // 6
                    col = i % 6
                    if stat in [division.pv,division.organisation]:
                        tk.Label(stats_frame, text=f"{abbr_stats[i]}:").grid(row=row * 2, column=col)
                        value = stat
                        if stat == division.pv: max_value = division._pv
                        if stat == division.organisation: max_value = division._organisation
                        progress = ttk.Progressbar(stats_frame, maximum=max_value, value=value, length=80)
                        progress.grid(row=row * 2 + 1, column=col)
                    else:
                        tk.Label(stats_frame, text=f"{abbr_stats[i]}: {stat}").grid(
                            row=row * 2, column=col)

                break

    def get_divisions_from_frame(self, frame):
        """
           Récupère les divisions à partir d'un cadre spécifié.
           Cette méthode extrait les noms des divisions à partir des enfants du cadre donné,
           puis recherche et retourne les instances de Division correspondantes.
           Args:
               frame (tk.Frame): Le cadre contenant les divisions.
           Retour:
               List[Division]: Une liste d'instances de la classe Division correspondant aux noms dans le cadre.
           """
        division_names = [child.winfo_children()[0].cget("text").split(":")[1].strip() for child in
                          frame.winfo_children()]
        return [
            next(
                (division for division in self.divisions if division.nom == name),
                None,
            )
            for name in division_names
        ]

    def open_division_selection(self, camp, frame):
        selection_window = tk.Toplevel(self)
        selection_window.title("Sélectionner une Division")
        selection_window.geometry("400x300")

        listbox = tk.Listbox(selection_window)
        listbox.pack(fill=tk.BOTH, expand=True)

        for division in self.divisions:
            listbox.insert(tk.END, division.template)

        def on_select():
            selected_name = tk.StringVar()
            selected_name.set(listbox.get(listbox.curselection()))
            self.add_division( frame, selected_name)
            #selection_window.destroy()

        tk.Button(selection_window, text="Ajouter", command=on_select).pack(pady=10)

    def save_battle_data(self):
        battle_data = {
            "weather": self.weather.get(),
            "terrain": self.terrain.get(),
            "leader_a": self.leader_a.get(),
            "leader_b": self.leader_b.get(),
            "camp_a": self.camp_a.get_data(),
            "camp_b": self.camp_b.get_data(),
            "log_text": self.log_text.get("1.0", tk.END).strip()
        }

        with open("battle_data.json", "w") as file:
            json.dump(battle_data, file, indent=4)

    def run_battle_round(self):
        """
            Exécute un round de bataille en utilisant les divisions de chaque camp.
            Cette méthode récupère les divisions de chaque camp, lance le calcul de la bataille,
            et affiche les résultats sous forme de log dans la zone de texte.
            Retour:
                None
            """
        # Ici tu ajoutes le code pour lancer le calcul de la bataille
        log_entry = "Résultats du round de bataille...\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

app = BattleWindow()
app.mainloop()