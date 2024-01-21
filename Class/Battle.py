from Class.Division import *
from Func.Tactics_func import *

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self, attacker, defender):
        '''
        Initialise l'objet bataille en chargeant les divisions
        :param attacker:
        :param defender:
        '''
        assert type(attacker) == Division and type(defender) == Division , "campA and campB must be division class"
        assert attacker.is_defending == False , "ATK.isDefending must be FALSE"
        assert defender.is_defending == True , "DEF.isDefending must be TRUE"
        self.attacker = attacker
        self.defender = defender
        self.attacker_tactic = None
        self.defender_tactic = None
        self.AttackerLeader = None
        self.DefenderLeader = None
        self.round_counter = 0
        self.Phase = "Default"

    def is_finnish(self):
        """
        Check si le combat est terminé
            - Si l'un des deux camps n'as plus de PV ou d'Organisation
        :return: True ou False
        """
        # Si PV ou orga des def ou attck est nulle ou moins alors fin de la bataille
        return any(val <= 0 for val in [self.attacker.pv,
                                        self.defender.pv,
                                        self.attacker.org,
                                        self.defender.org])

    def run(self, nb_rounds=1):
        """
        Vérifie les conditions pour lancer un round
        """
        assert type(nb_rounds) is int , "Nb must be an :int:"
        if nb_rounds != -1:
            i = 1
            while i <= nb_rounds and not self.is_finnish(): # Lancement de :Nb: rounds
                self.round()
                i += 1
        else: # Lancement des rounds jusqu'a fin du combat
            while not self.is_finnish():
                self.round()

    def round(self):
        """
        Lancement d'un round ATTAQUE et RIPOSTE (1h de combat dans HOI IV)
        """
        # Change de tactics tout les 12H
        if self.round_counter % 12 == 0:
            choose_tactic(self)
            txt = "New tactics / Battle phase: {}".format(self.Phase)
            txt += "\n- {} choose {} tactic".format(self.attacker.name, self.attacker_tactic)
            txt += "\n- {} choose {} tactic".format(self.defender.name, self.defender_tactic)

        # Round
        self.attacker.do_attack(self.defender)  # ATK attaque
        self.defender.take_damage(self.attacker)   # DEF prend les dommages
        self.defender.do_attack(self.attacker)  # DEF riposte
        self.attacker.take_damage(self.defender)   # ATK prend les dommages

        # Log de fin de round
        self.round_counter += 1
        self.print_log()

    def print_log(self):
        """
        log pour chaque heure de combats
            - résulat des PV et ORG de chaques divisions
        """
        txt = """----------- round {} -----------------
DivATK: {}/{}   {}/{}
DivDEF: {}/{}   {}/{}""".format(self.round_counter,
                                self.attacker.pv, self.attacker._PVMAX, self.attacker.org, self.attacker._ORG,
                                self.defender.pv, self.defender._PVMAX, self.defender.org, self.defender._ORG)
        if self.is_finnish():
            txt += """
----------- End of Battle -----------------
The battle finnish after {} hours
            """.format(self.round_counter)
        print(txt)