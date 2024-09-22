import tkinter as tk
import json
import os
from Classes.Division import Division



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

"""
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
"""