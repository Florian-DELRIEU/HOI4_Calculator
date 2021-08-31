from W40K_addon.W40K_Company import *

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self, ATK, DEF):
        assert type(ATK) == Company and type(DEF) == Company , "campA and campB must be division class"
        assert ATK.isDefending == False , "ATK.isDefending must be FALSE"
        assert DEF.isDefending == True ,  "DEF.isDefending must be TRUE"
        self.ATK = ATK
        self.DEF = DEF
        self.roundCounter = 0
        self.CAC_level = 0
    def isFinnish(self):
        """
        Check si le combat est terminé
            - Si l'un des deux camps n'as plus de PV ou d'Organisation
        :return: True ou False
        """
        if (self.ATK.HP <= 0) or (self.DEF.HP <= 0) or (self.ATK.ORG <= 0) or (self.DEF.ORG <= 0):
            return True
        else:
            return False
    def Round(self,Nb=1):
        """
        Definit le nombre de lancement de round
        :param Nb: Nombre de round souhaité (-1 si jusqu'a fin du combat)
        """
        assert type(Nb) is int , "Nb must be an :int:"
        if Nb != -1:
            i = 1
            while i <= Nb: # Lancement de :Nb: rounds
                self._Round()
                i += 1
        else: # Lancement des rounds jusqu'a fin du combat
            while not self.isFinnish():
                self._Round()
    def _Round(self):
        """
        Lancement d'une round ATTAQUE et RIPOSTE (1h de combat dans HOI IV)
        """
        self.ATK.Attaque(self.DEF,self.CAC_level)  # ATK attaque
        self.DEF.Damage(self.ATK,self.CAC_level)   # DEF prend les dommages
        self.DEF.Attaque(self.ATK,self.CAC_level)  # DEF riposte
        self.ATK.Damage(self.DEF,self.CAC_level)   # ATK prend les dommages
    # Log de fin de round
        self.roundCounter += 1
        self.printLOG()
    def printLOG(self):
        """
        log pour chaque heure de combats
            - résulat des PV et ORG de chaques divisions
        """
        txt = """----------- round {} -----------------
DivATK: {}/{}   {}/{}
DivDEF: {}/{}   {}/{}""".format(self.roundCounter,
                                self.ATK.PV,self.ATK.__HP,self.ATK.ORG,self.ATK.__ORG,
                                self.DEF.PV,self.DEF.__HP,self.DEF.ORG,self.DEF.__ORG)
        if self.isFinnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.roundCounter)
        print(txt)