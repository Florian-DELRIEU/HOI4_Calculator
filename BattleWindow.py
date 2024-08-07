import tkinter as tk
from tkinter import ttk
import json
import os
from Classes import Division,Camp
from TerrainList import terrain_list
import random

Division = Division.Division # shortcut
Camp = Camp.Camp # shortcut

class BattleWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fenêtre de Bataille")
        self.geometry("800x600")

        # Initialiser les camps
        self.camp_a = Camp()
        self.camp_a.is_attacking = True
        self.camp_b = Camp()
        self.camp_b.is_attacking = False

        # Charger les divisions sauvegardées
        self.divisions = self.load_divisions()

        # Cadre pour les paramètres de la bataille
        frame_params = tk.Frame(self)
        frame_params.pack(fill=tk.X, pady=10)

        tk.Label(frame_params, text="Météo").grid(row=0, column=0, padx=5)
        self.weather = tk.StringVar()
        tk.Entry(frame_params, textvariable=self.weather).grid(row=0, column=1, padx=5)

        self.terrain = None
        tk.Label(frame_params, text="Terrain").grid(row=0, column=2, padx=5)
        self.selected_terrain = tk.StringVar()
        self.selected_terrain.set(terrain_list[0].name)  # Set default terrain
        terrain_names = [terrain.name for terrain in terrain_list]
        self.terrain_dropdown = ttk.Combobox(frame_params, textvariable=self.selected_terrain, values=terrain_names)
        self.terrain_dropdown.grid(row=0, column=3, padx=5)
        self.terrain_dropdown.bind("<<ComboboxSelected>>", self.update_terrain())

        tk.Label(frame_params, text="Aire de combat").grid(row=2, column=0, padx=5)
        self.combat_width = tk.StringVar()
        self.combat_width.set(str(terrain_list[0].width))  # Set default width
        tk.Label(frame_params, textvariable=self.combat_width).grid(row=2, column=1, padx=5)

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

        self.round_counter = 0

    def load_divisions(self):
        """
           Charge les divisions sauvegardées à partir d'un fichier JSON.
           Cette méthode vérifie l'existence du fichier "divisions.json" et tente de charger les données JSON à partir de ce fichier.
           Les données sont ensuite converties en instances de la classe Division.
           Retour:
               List[Division]: Une liste d'instances de la classe Division représentant les divisions sauvegardées.
           """
        if os.path.exists("Saves/divisions.json"):
            with open("Saves/divisions.json", "r") as file:
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

                stats = [division._PV, division._ORGANISATION, division._SOFT_ATTACK, division._HARD_ATTACK, division._DEFENSE,
                         division._ATTAQUE, division.piercing, division.armor, division.hardness, division.width]
                abbr_stats = ["PV", "Org", "SA", "HA", "Def", "Atk", "Prc", "Arm", "Hard", "Wdth"]

                for i, stat in enumerate(stats):
                    row = i // 6
                    col = i % 6
                    if stat in [division._PV, division._ORGANISATION]:
                        tk.Label(stats_frame, text=f"{abbr_stats[i]}:").grid(row=row * 2, column=col)
                        value = stat
                        if stat == division._PV: max_value = division._PV
                        if stat == division._ORGANISATION: max_value = division._ORGANISATION
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

        with open("Saves/battle_data.json", "w") as file:
            json.dump(battle_data, file, indent=4)

    def update_terrain(self):
        """
        Recupère l'instance :terrain: a partir du choix fait dans le menu déroulant.
        :return:
        """
        selected_terrain_name = self.selected_terrain.get()
        for terrain in terrain_list:
            if terrain.name == selected_terrain_name:
                self.terrain = terrain

    def run_battle_round(self):
        """
            Exécute un round de bataille en utilisant les divisions de chaque camp.
            Cette méthode récupère les divisions de chaque camp, lance le calcul de la bataille,
            et affiche les résultats sous forme de log dans la zone de texte.
            Retour:
                None
            """
        # Ici tu ajoutes le code pour lancer le calcul de la bataille
        if self.round_counter == 0: self.move_in_frontline()
        self._round()
        log_entry = "Résultats du round de bataille...\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    def _round(self):
        """
        Mecanique des rounds
        :return:
        """
        camp_attacker = [camp for camp in [self.camp_a, self.camp_b] if camp.is_attacking][0]
        camp_defender = [camp for camp in [self.camp_a, self.camp_b] if not camp.is_attacking][0]
        for attacking_division in camp_attacker.divisions:
            self.targetting(attacking_division,camp_defender)

    def targetting(self,attacking_division,enemy_divisions):
        engagement_width = attacking_division.width * 2
        target_list = []
        random.shuffle(enemy_divisions)

        total_width = 0
        for enemy in enemy_divisions:
            if total_width + enemy.width <= engagement_width:
                target_list.append(enemy)
                total_width = sum(division.width for division in target_list)
            elif total_width == 0:
                target_list.append(enemy)
                break
            if not any(enemy_divisions.divisions.width << engagement_width):
                target_list.append(random.choice(enemy_divisions.divisions))




    def move_in_frontline(self):
        """
            Sélectionne les divisions des camps pour l'engagement en frontline en fonction de l'aire de combat
        :return:
        """
        for camp in [self.camp_a,self.camp_b]:
            # Move divisions in frontline
            available_divisions = [division for division in camp.divisions if division not in camp.in_frontline and division not in camp.in_reserves]
            for division in available_divisions:
                total_camp_width = sum(division.width for division in camp.in_frontline)
                if total_camp_width + division.width <= self.terrain.width:
                    camp.in_frontline.append(division)
            # Move divisions in reserves
            for division in camp.divisions:
                if division not in camp.in_frontline:
                    camp.in_reserves.append(division)

app = BattleWindow()
app.mainloop()