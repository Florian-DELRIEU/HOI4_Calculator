import tkinter as tk
from tkinter import ttk
from Library.TerrainList import terrain_list
from Library.LeaderList import *


def update_terrain(Battle, event=None):
    """
    Recupère l'instance :terrain: a partir du choix fait dans le menu déroulant.
    :return:
    """
    selected_terrain_name = Battle.selected_terrain.get()
    for terrain in terrain_list:
        if terrain.name == selected_terrain_name:
            Battle.terrain = terrain
            break
    update_combat_width(Battle)


def update_combat_width(Battle):
    """
    Mets à jour l'affichage du combat_width
    """
    Battle.combat_width = Battle.terrain.width
    try:
        Battle.combat_width *= Battle.camp_attacker.tactic.width_bonus * Battle.camp_defender.tactic.width_bonus
    except Exception:
        pass
    Battle.combat_width_display.set(str(Battle.combat_width))


def update_battle_info_display(Battle):
    """
    Met à jour l'affichage des tactiques pour chaque camp et la phase de bataille en cours.
    """
    Battle.attacker_tactic_label.config(text=f"Tactique Attaquant : {Battle.camp_attacker.tactic.name}")
    Battle.defender_tactic_label.config(text=f"Tactique Défenseur : {Battle.camp_defender.tactic.name}")
    Battle.battle_phase_label.config(text=f"Phase de Bataille : {Battle.battle_phase}")

def get_division_names(Battle):
    """
       Récupère les noms de toutes les divisions sauvegardées.
       Cette méthode parcourt la liste des divisions chargées et extrait le nom de chaque division.
       Retour:
           List[str]: Une liste contenant les noms de toutes les divisions sauvegardées.
       """
    return [division.template for division in Battle.divisions]


def add_division(Battle, frame, selected_division_var):
    """
       Ajoute une division au camp spécifié et affiche ses statistiques de manière compacte.

       Cette méthode recherche la division correspondant au nom sélectionné, crée un cadre pour la division,
       et affiche ses statistiques sous forme abrégée en colonnes, avec des barres de progression pour les PV et l'organisation.

       Args:
           frame (tk.Frame): Le cadre dans lequel ajouter la division (camp A ou camp B).
           selected_name (str): Le Nom de Template sélectionnée à ajouter.
       """
    # todo Ajouter les division directement dans la réserves via les bouttons
    if not (selected_name := selected_division_var.get()):
        return
    for division in Battle.divisions:
        if division.template == selected_name:
            camp = None
            if frame == Battle.camp_attacker_divisions_frame:
                Battle.camp_attacker.add_division(division)
                camp = Battle.camp_attacker
            if frame == Battle.camp_defender_divisions_frame:
                Battle.camp_defender.add_division(division)
                camp = Battle.camp_defender
            assert camp is not None, "camp is not assigned"
            frame_division = tk.Frame(frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
            frame_division.pack(fill=tk.X, pady=2)

            stats_frame = tk.Frame(frame_division)
            stats_frame.pack(fill=tk.X)

            display_division_stats(Battle,stats_frame, division, camp)


def open_division_selection(Battle, camp, frame):
    selection_window = tk.Toplevel(Battle)
    selection_window.title("Sélectionner une Division")
    selection_window.geometry("400x300")

    listbox = tk.Listbox(selection_window)
    listbox.pack(fill=tk.BOTH, expand=True)

    for division in Battle.divisions:
        listbox.insert(tk.END, division.template)

    def on_select():
        selected_name = tk.StringVar()
        selected_name.set(listbox.get(listbox.curselection()))
        Battle.add_division(frame, selected_name)
        # selection_window.destroy()

    tk.Button(selection_window, text="Ajouter", command=on_select).pack(pady=10)


def select_leader(Battle, camp_type):
    leader_window = tk.Toplevel(Battle)
    leader_window.title("Sélectionner un Leader")
    leader_window.geometry("300x200")

    listbox = tk.Listbox(leader_window)
    listbox.pack(fill=tk.BOTH, expand=True)

    # Remplir la liste avec les noms des leaders disponibles
    leaders = Battle.get_leaders()
    for leader in leaders:
        listbox.insert(tk.END, leader.name)  # Assurez-vous que les instances Leader ont un attribut `name`

    def on_select():
        selected_name = listbox.get(listbox.curselection())
        if camp_type == "attacker":
            Battle.attacker_leader_label.config(text=f"Leader Attaquant : {selected_name}")
            Battle.camp_attacker.add_leader(
                next((leader for leader in Battle.get_leaders() if leader.name == selected_name), None))
        else:
            Battle.defender_leader_label.config(text=f"Leader Défenseur : {selected_name}")
            Battle.camp_defender.add_leader(
                next((leader for leader in Battle.get_leaders() if leader.name == selected_name), None))
        leader_window.destroy()

    tk.Button(leader_window, text="Sélectionner", command=on_select).pack(pady=10)

def get_divisions_from_frame(Battle, frame):
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
            (division for division in Battle.divisions if division.nom == name),
            None,
        )
        for name in division_names
    ]

def display_division_stats(Battle ,stats_frame ,division ,camp):
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
            # FIXME -  TRUE lorsque :stat: à la meme valeur que :pv: ou :org:
            tk.Label(stats_frame, text=f"{abbr_stats[i]}: {stat}").grid(row=row * 2, column=col)
            value = stat
            if stat == division.pv: max_value = division._PV
            if stat == division.organisation: max_value = division._ORGANISATION
            progress = ttk.Progressbar(stats_frame, maximum=max_value, value=value, length=80)
            progress.grid(row=row * 2 + 1, column=col)
        else:
            tk.Label(stats_frame, text=f"{abbr_stats[i]}: {stat}").grid(row=row * 2, column=col)

def refresh_display(Battle):
    for frame, current_camp in [(Battle.camp_attacker_divisions_frame, Battle.camp_attacker),
                                (Battle.camp_defender_divisions_frame, Battle.camp_defender)]:
        for widget in frame.winfo_children():
            widget.destroy()  # Effacer les anciennes stats

        for division in current_camp.get_divisions():
            division_frame = tk.Frame(frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
            division_frame.pack(fill=tk.X, pady=2)
            stats_frame = tk.Frame(division_frame)
            stats_frame.pack(fill=tk.X)
            display_division_stats(Battle,stats_frame, division, current_camp)

def get_leaders(Battle):
    """
    Retourne la liste des leaders disponibles pour le camp spécifié.
    """
    return [leader_A, leader_B, leader_C, leader_D, no_leader]


def on_river_change(Battle):
    Battle.terrain.has_small_river = Battle.small_river_box.get()
    Battle.terrain.has_large_river = Battle.large_river_box.get()


def on_encirclement_change(Battle):
    Battle.encirclement = Battle.encirclement_box.get()