
class Division:
    def __init__(self):
        self._PVmax = 200
        self.PV = self._PVmax
        self.ORG = 100
        self.SA = 100 # Soft Attack
        self.HA = 10 # Hard Attack
        self.DEF = 50 # Defense
        self.BRK = 40 # Breakthought
        self.PRC = 10 # Piercing
        self.ARM = 10 # Armor
        self.HARD = 0.1 # Hardness
        self.RTCH = 0 # Retranchement
        self.STR = 1

    def ATT(self,Target=Division):
        self.STR = self.PV / self._PVmax
        NbATK = self.STR * (Target.HARD*self.HA + (1-Target.HARD)*self.SA)
    # Piercing ?
        if self.PRC <= Target.ARM: NbATK /= 2
    # Defense
        if Target.DEF > 