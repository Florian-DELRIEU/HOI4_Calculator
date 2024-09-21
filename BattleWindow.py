import tkinter as tk
from tkinter import ttk
import json
import os
from Classes import Division,Camp
from Functions.TacticsFunctions import choose_tactic, change_weight
from Library.TerrainList import terrain_list
from Library import LeaderList
from Library.LeaderList import *

Division = Division.Division # shortcut
Camp = Camp.Camp # shortcut

class BattleWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fenêtre de Bataille")
        self.geometry("1000x800")

        self.battle_phase = "Default"
        self.extra_side = tk.IntVar(value=0)
        self.fort_level = tk.IntVar(value=0)


        # Variables pour les cases à cocher (Petite et Grande Rivière)
        self.small_river_box = tk.BooleanVar()
        self.large_river_box = tk.BooleanVar()

        # Initialiser les camps
        self.camp_attacker = Camp()
        self.camp_attacker.is_attacking = True
        self.camp_defender = Camp()
        self.camp_defender.is_attacking = False

        # Charger les divisions sauvegardées
        self.divisions = self.load_divisions()

        # Cadre pour les paramètres de la bataille
        frame_params = tk.Frame(self)
        frame_params.pack(fill=tk.X, pady=10)

        # Ajouter une frame pour les leaders
        self.frame_leaders = tk.Frame(self)
        self.frame_leaders.pack(fill=tk.X, pady=10)

        # Label pour le leader du camp attaquant
        self.attacker_leader_label = tk.Label(self.frame_leaders, text="Leader Attaquant : Aucun",
                                              font=("Arial", 12, "bold"), bd=2, relief=tk.RIDGE)
        self.attacker_leader_label.pack(side=tk.LEFT, padx=20)
        self.attacker_leader_label.bind("<Button-1>", lambda event: self.select_leader("attacker"))

        # Label pour le leader du camp défenseur
        self.defender_leader_label = tk.Label(self.frame_leaders, text="Leader Défenseur : Aucun",
                                              font=("Arial", 12, "bold"), bd=2, relief=tk.RIDGE)
        self.defender_leader_label.pack(side=tk.RIGHT, padx=20)
        self.defender_leader_label.bind("<Button-1>", lambda event: self.select_leader("defender"))

        # Ajout des labels pour les tactiques et la phase de bataille
        self.battle_phase_label = tk.Label(self, text="Phase de Bataille : Aucune", font=("Arial", 12, "bold"))
        self.battle_phase_label.pack(side=tk.TOP, pady=5)

        # Créer un cadre pour les labels de tactiques
        frame_tactics = tk.Frame(self)
        frame_tactics.pack(fill=tk.X, pady=10)

        # Label pour la tactique du camp attaquant (à gauche)
        self.attacker_tactic_label = tk.Label(frame_tactics, text="Tactique Attaquant : Aucune",
                                                                                            font=("Arial", 12, "bold"))
        self.attacker_tactic_label.pack(side=tk.LEFT, padx=20)

        # Label pour la tactique du camp défenseur (à droite)
        self.defender_tactic_label = tk.Label(frame_tactics, text="Tactique Défenseur : Aucune",
                                                                                            font=("Arial", 12, "bold"))
        self.defender_tactic_label.pack(side=tk.RIGHT, padx=20)

        tk.Label(frame_params, text="Météo").grid(row=0, column=0, padx=5)
        self.weather = tk.StringVar()
        tk.Entry(frame_params, textvariable=self.weather).grid(row=0, column=1, padx=5)

        self.terrain = terrain_list[0]
        tk.Label(frame_params, text="Terrain").grid(row=0, column=2, padx=5)
        self.selected_terrain = tk.StringVar()
        self.selected_terrain.set(terrain_list[0].name)  # Set default terrain
        terrain_names = [terrain.name for terrain in terrain_list]
        self.terrain_dropdown = ttk.Combobox(frame_params, textvariable=self.selected_terrain, values=terrain_names)
        self.terrain_dropdown.grid(row=0, column=3, padx=5)
        self.terrain_dropdown.bind("<<ComboboxSelected>>", self.update_terrain)

        # Ajouter les cases à cocher pour les rivières
        tk.Checkbutton(frame_params, text="Petite Rivière", variable=self.small_river_box,
                       command=self.on_river_change).grid(row=0, column=4, padx=5)
        tk.Checkbutton(frame_params, text="Grande Rivière", variable=self.large_river_box,
                       command=self.on_river_change).grid(row=1, column=4, padx=5)

        self.combat_width = terrain_list[0].width
        tk.Label(frame_params, text="Aire de combat").grid(row=2, column=0, padx=5)
        self.combat_width_display = tk.StringVar()
        self.combat_width_display.set(str(self.combat_width))  # Set default width
        tk.Label(frame_params, textvariable=self.combat_width_display).grid(row=2, column=1, padx=5)

        # Ajouter le Spinbox pour "Autres directions d'attaques" (assumons que vous avez déjà ce Spinbox)
        tk.Label(frame_params, text="Autres directions d'attaques").grid(row=1, column=0, padx=5)
        attack_directions_spinbox = tk.Spinbox(frame_params, from_=0, to=10, textvariable=self.extra_side)
        attack_directions_spinbox.grid(row=1, column=1, padx=5)

        # Ajouter le Spinbox pour "Niveaux de Fortification" juste à côté
        tk.Label(frame_params, text="Niveaux de Fortification").grid(row=1, column=2, padx=5)
        fortification_spinbox = tk.Spinbox(frame_params, from_=0, to=5, textvariable=self.fort_level)
        fortification_spinbox.grid(row=1, column=3, padx=5)

        # Cadre pour les camps
        frame_battle = tk.Frame(self)
        frame_battle.pack(fill=tk.BOTH, expand=True, pady=10)

        # Camp A
        frame_camp_attacker = tk.Frame(frame_battle)
        frame_camp_attacker.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(frame_camp_attacker, text="Camp Attacker").pack()
        self.camp_attacker_divisions_frame = tk.Frame(frame_camp_attacker)
        self.camp_attacker_divisions_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Button(frame_camp_attacker, text="Ajouter Division", command=lambda: self.open_division_selection(self.camp_attacker, self.camp_attacker_divisions_frame)).pack()

        # Camp B
        frame_camp_defender = tk.Frame(frame_battle)
        frame_camp_defender.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(frame_camp_defender, text="Camp Defender").pack()
        self.camp_defender_divisions_frame = tk.Frame(frame_camp_defender)
        self.camp_defender_divisions_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Button(frame_camp_defender, text="Ajouter Division", command=lambda: self.open_division_selection(self.camp_defender, self.camp_defender_divisions_frame)).pack()

        # Bouton pour lancer un round de la bataille
        tk.Button(self, text="Lancer un Round", command=self.run_battle_round).pack(pady=10)
        tk.Button(self, text="Sauvegarder Bataille", command=self.save_battle_data).pack(pady=10)

        # Zone de logs pour les résultats
        self.log_text = tk.Text(self, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.round_counter = 0

        self.camp_defender.get_battle_info(self)
        self.camp_attacker.get_battle_info(self)

    ############# ROUNDS ####################

    def run_battle_round(self):
        """
            Exécute un round de bataille en utilisant les divisions de chaque camp.
            Cette méthode récupère les divisions de chaque camp, lance le calcul de la bataille,
            et affiche les résultats sous forme de log dans la zone de texte.
            Retour:
                None
            """
        # Mets a jour battle infos
        self.camp_defender.get_battle_info(self)
        self.camp_attacker.get_battle_info(self)

        # Round initial
        if self.round_counter == 0:
            for camp in [self.camp_attacker,self.camp_defender]:
                camp.get_battle_info(self)
                camp.move_in_frontline()
        if self.round_counter % 12 == 0:
            self.tactic_round()
        self._round(self.camp_attacker,self.camp_defender)
        # Vérification états de chaque division et renforts ?

        self.check_state_of_division()
        self.renfort_round()
        # Ecriture des logs
        log_entry = "Résultats du round de bataille...\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.round_counter += 1

        # Mets a jour affichage
        self.refresh_display()
        self.update_battle_info_display()
        self.update_combat_width()


    def _round(self,camp_attacker,camp_defender):
        """
        Mecanique des rounds
        :return:
        """
        # Todo
        #  - Verifier si la riposte du défenseur est fait correctement selon les mécaniques du jeu

        # Tour Attaquant
        for division in camp_attacker.frontline:
            division.targeting(camp_defender)
            division.do_attack(self)
        # Tour Defenseur
        for division in camp_defender.frontline:
            division.targeting(camp_attacker)
            division.do_attack(self)

    def renfort_round(self):
        for camp in [self.camp_attacker,self.camp_defender]:
            camp.from_reserve_to_frontline()

    def tactic_round(self):
        choose_tactic(self)

    def check_state_of_division(self):
        """
        Vérifie si une division n'as plus de PV ou ORG
        :return: Si oui alors fait appel à la méthode self.retreat_division()
        """
        for camp in [self.camp_attacker,self.camp_defender]:
            for division in camp.divisions:
                if division.pv <= 0 or division.organisation <= 0:
                    self.retreat_division(division)

###################################################
    def retreat_division(self,division_to_retreat):
        """
        Retire la division de toute les listes de la bataille. Pour représenté que la division s'est replié du champ de
        bataille.
        :param division_to_retreat: Division qui doit se replier par manque d'organisation ou de PV
        """
        for camp in [self.camp_attacker,self.camp_defender]:
            if division_to_retreat in camp.frontline:   camp.frontline.remove(division_to_retreat)
            if division_to_retreat in camp.reserves:    camp.reserves.remove(division_to_retreat)
            if division_to_retreat in camp.divisions:   camp.divisions.remove(division_to_retreat)
            for division in camp.divisions:
                if division_to_retreat in division.target_list:     division.target_list.remove(division_to_retreat)
                if division_to_retreat == division.primary_target:  division.primary_target = None

        # Supprime l'affichage de la division
        for frame in [self.camp_attacker_divisions_frame, self.camp_defender_divisions_frame]:
            for widget in frame.winfo_children():
                # Comparer les widgets avec la division
                if isinstance(widget, tk.Frame) and widget.winfo_children():
                    stats_label = widget.winfo_children()[0]  # Le premier enfant est souvent le label des stats
                    if isinstance(stats_label, tk.Label) and stats_label.cget("text").startswith(
                            division_to_retreat.template):
                        widget.destroy()  # Détruire le cadre correspondant à la division retirée
                        break

    def update_terrain(self,event=None):
        """
        Recupère l'instance :terrain: a partir du choix fait dans le menu déroulant.
        :return:
        """
        selected_terrain_name = self.selected_terrain.get()
        for terrain in terrain_list:
            if terrain.name == selected_terrain_name:
                self.terrain = terrain
                break
        self.update_combat_width()

    def update_combat_width(self):
        """
        Mets à jour l'affichage du combat_width
        """
        self.combat_width = self.terrain.width
        try:
            self.combat_width *= self.camp_attacker.tactic.width_bonus * self.camp_defender.tactic.width_bonus
        except Exception:
            pass
        self.combat_width_display.set(str(self.combat_width))

    def update_battle_info_display(self):
        """
        Met à jour l'affichage des tactiques pour chaque camp et la phase de bataille en cours.
        """
        self.attacker_tactic_label.config(text=f"Tactique Attaquant : {self.camp_attacker.tactic.name}")
        self.defender_tactic_label.config(text=f"Tactique Défenseur : {self.camp_defender.tactic.name}")
        self.battle_phase_label.config(text=f"Phase de Bataille : {self.battle_phase}")


    ############# BOUTONS ####################

    def load_divisions(self):
        """
           Charge les divisions sauvegardées à partir d'un fichier JSON.
           Cette méthode vérifie l'existence du fichier "divisions.json" et tente de charger les données JSON à partir
           de ce fichier.
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
        #todo Ajouter les division directement dans la réserves via les bouttons
        if not (selected_name := selected_division_var.get()):
            return
        for division in self.divisions:
            if division.template == selected_name:
                camp = None
                if frame == self.camp_attacker_divisions_frame:
                    self.camp_attacker.add_division(division)
                    camp = self.camp_attacker
                if frame == self.camp_defender_divisions_frame:
                    self.camp_defender.add_division(division)
                    camp = self.camp_defender
                assert camp is not None , "camp is not assigned"
                frame_division = tk.Frame(frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
                frame_division.pack(fill=tk.X, pady=2)

                stats_frame = tk.Frame(frame_division)
                stats_frame.pack(fill=tk.X)

                self.display_division_stats(stats_frame,division,camp)

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
            "leader_a": self.leader_attacker.get(),
            "leader_b": self.leader_defender.get(),
            "camp_a": self.camp_attacker.get_data(),
            "camp_b": self.camp_defender.get_data(),
            "log_text": self.log_text.get("1.0", tk.END).strip()
        }

        with open("Saves/battle_data.json", "w") as file:
            json.dump(battle_data, file, indent=4)

    def display_division_stats(self,stats_frame,division,camp):
        # Déterminer la couleur en fonction de la position de la division
        if division in camp.frontline:
            bg_color = "lightblue"  # Couleur pour les divisions en frontline
        elif division in camp.reserves:
            bg_color = "lightgray"  # Couleur pour les divisions en réserves
        else:
            bg_color = "white"  # Couleur par défaut si la division n'est ni en frontline ni en réserves

        # Appliquer la couleur de fond
        stats_frame.configure(bg=bg_color)

        stats = [division.pv, division.organisation, division.soft_attack, division.hard_attack, division.defense,
                 division.attaque, division.piercing, division.armor, division.hardness, division.width]
        abbr_stats = ["PV", "Org", "SA", "HA", "Def", "Atk", "Prc", "Arm", "Hard", "Wdth"]

        for i, stat in enumerate(stats):
            row = i // 6
            col = i % 6
            if stat in [division.pv, division.organisation]:
                #FIXME -  TRUE lorsque :stat: à la meme valeur que :pv: ou :org:
                tk.Label(stats_frame, text=f"{abbr_stats[i]}: {stat}").grid(row=row * 2, column=col)
                value = stat
                if stat == division.pv: max_value = division._PV
                if stat == division.organisation: max_value = division._ORGANISATION
                progress = ttk.Progressbar(stats_frame, maximum=max_value, value=value, length=80)
                progress.grid(row=row * 2 + 1, column=col)
            else:
                tk.Label(stats_frame, text=f"{abbr_stats[i]}: {stat}").grid(row=row * 2, column=col)

    def refresh_display(self):
        for frame, current_camp in [(self.camp_attacker_divisions_frame, self.camp_attacker),
                                    (self.camp_defender_divisions_frame, self.camp_defender)]:
            for widget in frame.winfo_children():
                widget.destroy()  # Effacer les anciennes stats

            for division in current_camp.get_divisions():
                division_frame = tk.Frame(frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
                division_frame.pack(fill=tk.X, pady=2)
                stats_frame = tk.Frame(division_frame)
                stats_frame.pack(fill=tk.X)
                self.display_division_stats(stats_frame, division, current_camp)

    def select_leader(self, camp_type):
        leader_window = tk.Toplevel(self)
        leader_window.title("Sélectionner un Leader")
        leader_window.geometry("300x200")

        listbox = tk.Listbox(leader_window)
        listbox.pack(fill=tk.BOTH, expand=True)

        # Remplir la liste avec les noms des leaders disponibles
        leaders = self.get_leaders()
        for leader in leaders:
            listbox.insert(tk.END, leader.name)  # Assurez-vous que les instances Leader ont un attribut `name`

        def on_select():
            selected_name = listbox.get(listbox.curselection())
            if camp_type == "attacker":
                self.attacker_leader_label.config(text=f"Leader Attaquant : {selected_name}")
                self.camp_attacker.add_leader(next((leader for leader in self.get_leaders() if leader.name == selected_name), None))
            else:
                self.defender_leader_label.config(text=f"Leader Défenseur : {selected_name}")
                self.camp_defender.add_leader(next((leader for leader in self.get_leaders() if leader.name == selected_name), None))
            leader_window.destroy()

        tk.Button(leader_window, text="Sélectionner", command=on_select).pack(pady=10)

    def get_leaders(self):
        """
        Retourne la liste des leaders disponibles pour le camp spécifié.
        """
        return [leader_A, leader_B, leader_C, leader_D, no_leader]

    def on_river_change(self):
        self.terrain.has_small_river = self.small_river_box.get()
        self.terrain.has_large_river = self.large_river_box.get()


app = BattleWindow()

test_case = "Case 1"
if __name__ == "__main__" and test_case == "Case 1":
    app.camp_attacker.add_leader(LeaderList.leader_A)
    app.attacker_leader_label.config(text=f"Leader Attaquant : {app.camp_attacker.leader.name}")
    app.camp_defender.add_leader(LeaderList.no_leader)
    app.defender_leader_label.config(text=f"Leader Defenseur : {app.camp_defender.leader.name}")
    app.add_division(app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. A1"
    app.add_division(app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. A2"
    app.add_division(app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. A3"
    app.add_division(app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_defender.get_divisions()[-1].nom = "Div. B1"
    app.add_division(app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_defender.get_divisions()[-1].nom = "Div. B2"
    app.add_division(app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_defender.get_divisions()[-1].nom = "Div. B3"

if __name__ == "__main__" and test_case == "Case 2":
    app.camp_attacker.add_leader(LeaderList.no_leader)
    app.attacker_leader_label.config(text=f"Leader Attaquant : {app.camp_attacker.leader.name}")
    app.camp_defender.add_leader(LeaderList.no_leader)
    app.defender_leader_label.config(text=f"Leader Defenseur : {app.camp_defender.leader.name}")
    app.add_division(app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. A"
    app.add_division(app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. B"
app.mainloop()