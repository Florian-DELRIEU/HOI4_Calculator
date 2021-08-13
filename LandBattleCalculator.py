
class Division:
    def __init__(self):
        self._PVmax = 200
        self._ORG = 100
        self._SA = 100 # Soft Attack
        self._HA = 10 # Hard Attack
        self._DEF = 50 # Defense
        self._BRK = 40 # Breakthought
        self.PV = self._PVmax
        self.ORG = 100
        self.PRC = 10 # Piercing
        self.ARM = 10 # Armor
        self.HARD = 0.1 # Hardness
        self.RTCH = 0 # Retranchement
        self.NbATK = 0
        self.set_STR()
        self.isDefending = False

    def set_STR(self):
        self.STR = self.PV / self._PVmax
        self.SA = self._SA * self.STR
        self.HA = self._HA * self.STR
        self.DEF = self._DEF * self.STR
        self.BRK = self._BRK * self.STR

    def Attaque(self,Target):
        self.set_STR()
        NbATK = Target.HARD*self.HA + (1-Target.HARD)*self.SA
    # Piercing ?
        if self.PRC <= Target.ARM: NbATK /= 2
        self.NbATK = NbATK

    def Damage(self,Striker):
    # Calcul nombre de touche
        self.set_STR()
        NbDAMAGE = Striker.NbATK
        if self.isDefending:
            DEF = self.DEF
        else:
            DEF = self.BRK
        if self.DEF > NbDAMAGE: NbDAMAGE *= 0.1
        else:                   NbDAMAGE = self.DEF*0.1 + (NbDAMAGE-self.DEF)*0.6
    # Calcul des dégats entre les PV et l'ORG
        self.PV -= 1.5*NbDAMAGE
        if self.PV <= 0 : self.PV = 0
        self.ORG -= 2.5*NbDAMAGE
        if self.ORG <= 0 : self.ORG = 0

class Battle:
    def __init__(self, ATK, DEF):
        assert type(ATK) == Division and type(DEF) == Division , "campA and campB must be division class"
        assert ATK.isDefending == False , "ATK.isDefending must be FALSE"
        assert DEF.isDefending == True ,  "DEF.isDefending must be TRUE"
        self.ATK = ATK
        self.DEF = DEF

    def Round(self):
        self.ATK.Attaque(self.DEF)
        self.DEF.Damage(self.ATK)
        self.DEF.Attaque(self.ATK)
        self.ATK.Damage(self.DEF)

        self.printLOG()

    def printLOG(self):
        txt = """
        DivATK: {}/{}   {}/{}
        DivDEF: {}/{}   {}/{}
        """.format(self.ATK.PV,self.ATK._PVmax,self.ATK.ORG,self.ATK._ORG,
                   self.DEF.PV,self.DEF._PVmax,self.DEF.ORG,self.DEF._ORG)

        print(txt)


####### TESTING

DivA = Division()
DivA.isDefending = False
DivB = Division()
DivB.isDefending = True

BATTLE = Battle(DivA,DivB)
BATTLE.Round()