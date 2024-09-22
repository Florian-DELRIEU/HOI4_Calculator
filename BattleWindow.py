import tkinter as tk
from tkinter import ttk
from Classes.Camp import Camp
from Functions.TacticsFunctions import choose_tactic
from Functions.UI_functions import *
from Functions.SavingFunctions import *
from Library.TerrainList import terrain_list
from Library import LeaderList
from Library.LeaderList import *


class BattleWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fenêtre de Bataille")
        self.geometry("1000x800")

        self.battle_phase = "Default"
        self.extra_side = tk.IntVar(value=0)
        self.fort_level = tk.IntVar(value=0)


        # Variables pour les cases à cocher (Petite et Grande Rivière)
        self.small_river_box  = tk.BooleanVar()
        self.large_river_box  = tk.BooleanVar()
        self.encirclement_box = tk.BooleanVar()

        # Initialiser les camps
        self.camp_attacker = Camp()
        self.camp_attacker.is_attacking = True
        self.camp_defender = Camp()
        self.camp_defender.is_attacking = False

        # Charger les divisions sauvegardées
        self.divisions = load_divisions(self)

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
        self.attacker_leader_label.bind("<Button-1>", lambda event: select_leader(self,"attacker"))

        # Label pour le leader du camp défenseur
        self.defender_leader_label = tk.Label(self.frame_leaders, text="Leader Défenseur : Aucun",
                                              font=("Arial", 12, "bold"), bd=2, relief=tk.RIDGE)
        self.defender_leader_label.pack(side=tk.RIGHT, padx=20)
        self.defender_leader_label.bind("<Button-1>", lambda event: select_leader(self,"defender"))

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
        self.combat_width_display = tk.StringVar()
        self.combat_width = terrain_list[0].width
        self.terrain_dropdown.bind("<<ComboboxSelected>>", update_terrain(self))

        # Ajouter les cases à cocher pour les rivières
        tk.Checkbutton(frame_params, text="Petite Rivière", variable=self.small_river_box,
                       command=on_river_change(self)).grid(row=0, column=4, padx=5)
        tk.Checkbutton(frame_params, text="Grande Rivière", variable=self.large_river_box,
                       command=on_river_change(self)).grid(row=1, column=4, padx=5)
        tk.Checkbutton(frame_params, text="Encerclement", variable=self.encirclement_box,
                       command=on_encirclement_change(self)).grid(row=0, column=5, padx=5)

        tk.Label(frame_params, text="Aire de combat").grid(row=2, column=0, padx=5)
        self.combat_width_display.set(str(self.combat_width))  # Set default width
        tk.Label(frame_params, textvariable=self.combat_width_display).grid(row=2, column=1, padx=5)

        # Ajouter le Spinbox pour "Autres directions d'attaques" (assumons que vous avez déjà ce Spinbox)
        tk.Label(frame_params, text="Autres directions d'attaques").grid(row=1, column=0, padx=5)
        attack_directions_spinbox = tk.Spinbox(frame_params, from_=0, to=5, textvariable=self.extra_side)
        attack_directions_spinbox.grid(row=1, column=1, padx=5)

        # Ajouter le Spinbox pour "Niveaux de Fortification" juste à côté
        tk.Label(frame_params, text="Niveaux de Fortification").grid(row=1, column=2, padx=5)
        fortification_spinbox = tk.Spinbox(frame_params, from_=0, to=10, textvariable=self.fort_level)
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

        tk.Button(frame_camp_attacker, text="Ajouter Division", command=lambda: open_division_selection(self,self.camp_attacker, self.camp_attacker_divisions_frame)).pack()

        # Camp B
        frame_camp_defender = tk.Frame(frame_battle)
        frame_camp_defender.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(frame_camp_defender, text="Camp Defender").pack()
        self.camp_defender_divisions_frame = tk.Frame(frame_camp_defender)
        self.camp_defender_divisions_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Button(frame_camp_defender, text="Ajouter Division", command=lambda: open_division_selection(self,self.camp_defender, self.camp_defender_divisions_frame)).pack()

        # Bouton pour lancer un round de la bataille
        tk.Button(self, text="Lancer un Round", command=self.run_battle_round).pack(pady=10)
        #tk.Button(self, text="Sauvegarder Bataille", command=save_battle_data(self)).pack(pady=10)

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
        refresh_display(self)
        update_battle_info_display(self)
        update_combat_width(self)


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




    ############# BOUTONS ####################



app = BattleWindow()

test_case = "Case 1"
if __name__ == "__main__" and test_case == "Case 1":
    app.camp_attacker.add_leader(LeaderList.leader_A)
    app.attacker_leader_label.config(text=f"Leader Attaquant : {app.camp_attacker.leader.name}")
    app.camp_defender.add_leader(LeaderList.no_leader)
    app.defender_leader_label.config(text=f"Leader Defenseur : {app.camp_defender.leader.name}")
    add_division(app,app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. A1"
    add_division(app,app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. A2"
    add_division(app,app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. A3"
    add_division(app,app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_defender.get_divisions()[-1].nom = "Div. B1"
    add_division(app,app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_defender.get_divisions()[-1].nom = "Div. B2"
    add_division(app,app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_defender.get_divisions()[-1].nom = "Div. B3"

if __name__ == "__main__" and test_case == "Case 2":
    app.camp_attacker.add_leader(LeaderList.no_leader)
    app.attacker_leader_label.config(text=f"Leader Attaquant : {app.camp_attacker.leader.name}")
    app.camp_defender.add_leader(LeaderList.no_leader)
    app.defender_leader_label.config(text=f"Leader Defenseur : {app.camp_defender.leader.name}")
    add_division(app,app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. A"
    add_division(app,app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.camp_attacker.get_divisions()[-1].nom = "Div. B"
app.mainloop()