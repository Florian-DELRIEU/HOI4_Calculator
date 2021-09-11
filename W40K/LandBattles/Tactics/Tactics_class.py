class Tactic:
    def __init__(self,SA=1,HA=1,SMA=1,HMA=1,BRK=1,DEF=1,CAC=0,isDefenseTactic=True,Name=""):
        self.Name = Name
    # is Defense ?
        self.isDefenseTactic = isDefenseTactic
    # Bonus
        self.Bonus_SA = SA
        self.Bonus_HA = HA
        self.Bonus_SMA = SMA
        self.Bonus_HMA = HMA
        self.Bonus_BRK = BRK
        self.Bonus_DEF = DEF
    # CAC
        self.CAC = CAC

    def __repr__(self):
        return self.Name