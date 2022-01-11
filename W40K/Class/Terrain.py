from MyPack2.Utilities import truncDecimal

class Terrain():
    def __init__(self,Combat_Witdth=(90,45),Attrition=0,AttackMalus=0,AirSuperiorityMalus=0):
        self.Type = "Plains"
        self.RiverCrossing = False
        self.Combat_width = Combat_Witdth
        self.Attrition = Attrition
        self.Attack_malus = AttackMalus
        self.Defense_malus = 0
        self.AirSuperiorityMalus = AirSuperiorityMalus
        self.Fort_level = 0
        self.River = None

    def set_River(self,river_width):
        assert river_width == ("Small" or "Big" or None) , "river-width must be 'Small', 'big' or 'None' "
        self.River = river_width
        self.RiverCrossing = self.River is not None
        if   self.River == "Small": self.Attack_malus *= (1-0.3)
        elif self.River == "Big"  : self.Attack_malus *= (1-0.6)
        self.Attack_malus = truncDecimal(self.Attack_malus,2)
        self.Defense_malus = self.Attack_malus
