class Tactic:
    def __init__(self,ATK_Damage=1,ATK_Defense=1,DEF_Damage=1,DEF_Defense=1,weight=4,CounteredBy=None,Name="",
                 BeginPhase=None):
        self.Name = Name
        self.CounteredBy = CounteredBy
    # Bonus
        self.ATK_Damage = ATK_Damage
        self.ATK_Defense = ATK_Defense
        self.DEF_Damage = DEF_Damage
        self.DEF_Defense = DEF_Defense
    # Begin battle phase
        self.weight = weight
        self.Begin_battle_phase = None

    def __repr__(self):
        return self.Name
    