from Library import LeaderList
from Functions.UI_functions import *
from BattleWindow import BattleWindow
import tkinter as tk

app = BattleWindow()

test_case = "Case 1"
if __name__ == "__main__":
    if test_case == "Case 1":
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

    elif test_case == "Case 2":
        app.camp_attacker.add_leader(LeaderList.no_leader)
        app.attacker_leader_label.config(text=f"Leader Attaquant : {app.camp_attacker.leader.name}")
        app.camp_defender.add_leader(LeaderList.no_leader)
        app.defender_leader_label.config(text=f"Leader Defenseur : {app.camp_defender.leader.name}")
        add_division(app,app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
        app.camp_attacker.get_divisions()[-1].nom = "Div. A"
        add_division(app,app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
        app.camp_attacker.get_divisions()[-1].nom = "Div. B"
app.mainloop()