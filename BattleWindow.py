import tkinter as tk
from tkinter import ttk
import json
import os
from Class import Division,Camp
from tkinter import messagebox

class BattleWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fenêtre de Bataille")
        self.geometry("800x600")

        # Charger les divisions sauvegardées
        self.divisions = self.load_divisions()

        # Instance des camps
        self.Camp_A = Camp
        self.Camp_B = Camp

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
        self.Camp_A.leader = tk.StringVar()
        tk.Entry(frame_params, textvariable=self.Camp_A.leader).grid(row=1, column=1, padx=5)

        tk.Label(frame_params, text="Leader Camp B").grid(row=1, column=2, padx=5)
        self.Camp_B.leader = tk.StringVar()
        tk.Entry(frame_params, textvariable=self.Camp_B.leader).grid(row=1, column=3, padx=5)

        # Cadre pour les camps
        frame_battle = tk.Frame(self)
        frame_battle.pack(fill=tk.BOTH, expand=True, pady=10)

        # Camp A
        frame_camp_a = tk.Frame(frame_battle)
        frame_camp_a.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        self.Camp_A.frame = frame_camp_a

        tk.Label(frame_camp_a, text="Camp A").pack()
        self.camp_a_divisions = tk.Frame(frame_camp_a)
        self.camp_a_divisions.pack(fill=tk.BOTH, expand=True, pady=5)

        self.add_division_a = tk.StringVar()
        dropdown_a = ttk.Combobox(frame_camp_a, textvariable=self.add_division_a, values=self.get_division_names())
        dropdown_a.pack(pady=5)
        tk.Button(frame_camp_a, text="Ajouter Division", command=lambda: self.add_division(self.add_division_a, self.Camp_A)).pack()

        # Camp B
        frame_camp_b = tk.Frame(frame_battle)
        frame_camp_b.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        self.Camp_B.frame = frame_camp_b

        tk.Label(frame_camp_b, text="Camp B").pack()
        self.camp_b_divisions = tk.Frame(frame_camp_b)
        self.camp_b_divisions.pack(fill=tk.BOTH, expand=True, pady=5)

        self.add_division_b = tk.StringVar()
        dropdown_b = ttk.Combobox(frame_camp_b, textvariable=self.add_division_b, values=self.get_division_names())
        dropdown_b.pack(pady=5)
        tk.Button(frame_camp_b, text="Ajouter Division", command=lambda: self.add_division(self.add_division_b, self.Camp_B)).pack()

        # Bouton pour lancer un round de la bataille
        tk.Button(self, text="Lancer un Round", command=self.run_battle_round).pack(pady=10)

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

    def add_division(self, selected_division_var, camp=Camp()):
        # sourcery skip: assign-if-exp
        """
           Ajoute une division au camp spécifié et affiche ses statistiques de manière compacte.

           Cette méthode recherche la division correspondant au nom sélectionné, crée un cadre pour la division,
           et affiche ses statistiques sous forme abrégée en colonnes, avec des barres de progression pour les PV et l'organisation.

           Args:
               frame (tk.Frame): Le cadre dans lequel ajouter la division (camp A ou camp B).
               selected_name (str): Le Nom de Template sélectionnée à ajouter.
           """
        frame = camp.frame
        if not (selected_name := selected_division_var.get()):
            return
        for division in self.divisions:
            if division.template == selected_name:
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
                        if stat == division.pv:             max_value = division._pv
                        if stat == division.organisation:   max_value = division._organisation
                        else:                               max_value = None
                        progress = ttk.Progressbar(stats_frame, maximum=max_value, value=value, length=80)
                        progress.grid(row=row * 2 + 1, column=col)
                    else:
                        tk.Label(stats_frame, text=f"{abbr_stats[i]}: {stat}").grid(
                            row=row * 2, column=col)

                break
            camp.division_list.append(division)


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