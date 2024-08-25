import unittest
from BattleWindow import BattleWindow
import tkinter as tk


class add_adivision(unittest.TestCase):
    app = BattleWindow()
    app.add_division(app.camp_attacker_divisions_frame, tk.StringVar(value="Infanterie 36"))
    division_1 = app.camp_attacker.divisions[0]
    app.mainloop()

class battle_2v2(unittest.TestCase):
    app = BattleWindow()
    app.add_division(app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.add_division(app.camp_attacker_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.add_division(app.camp_defender_divisions_frame,tk.StringVar(value="Infanterie 36"))
    app.add_division(app.camp_defender_divisions_frame,tk.StringVar(value="Blindes 36"))
    app.mainloop()

if __name__ == '__main__':
    unittest.main()
