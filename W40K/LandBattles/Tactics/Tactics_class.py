class Tactic:
    def __init__(self,ATK_Damage=1,ATK_Defense=1,DEF_Damage=1,DEF_Defense=1,CAC=0,weight=1,Name=""):
        self.Name = Name
    # Bonus
        self.ATK_Damage = ATK_Damage
        self.ATK_Defense = ATK_Defense
        self.DEF_Damage = DEF_Damage
        self.DEF_Defense = DEF_Defense
    # CAC
        self.CAC = CAC
        self.weight = weight

    def __repr__(self):
        return self.Name
    