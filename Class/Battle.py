from Class.Division import *

class Battle:
    """
    Objet contenant les divisions permettant de lancer les round et les logs
    """
    def __init__(self, attacker, defender):
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
        return any(val <= 0 for val in [self.attacker.pv,
                                        self.defender.pv,
                                        self.attacker.org,
                                        self.defender.org])  # Si PV ou orga des def ou attck est nulle ou moins

    def run_rounds(self, nb_rounds=1):
        """
        Definit le nombre de lancement de round
        :param nb_rounds: Nombre de round souhaité (-1 si jusqu'a fin du combat)
        """
        assert type(nb_rounds) is int , "Nb must be an :int:"
        if nb_rounds != -1:
            i = 1
            while i <= nb_rounds: # Lancement de :Nb: rounds
                self._round()
                i += 1
        else: # Lancement des rounds jusqu'a fin du combat
            while not self.is_finnish():
                self._round()
    def _round(self):
        """
        Lancement d'un round ATTAQUE et RIPOSTE (1h de combat dans HOI IV)
        """
        if self.round_counter % 12 == 0:  # Choix de Tactique tout les 12 rounds
            choose_tactic(self)
            txt = "New tactics / Battle phase: {}".format(self.Phase)
            txt += "\n- {} choose {} tactic".format(self.attacker.name, self.attacker_tactic)
            txt += "\n- {} choose {} tactic".format(self.defender.name, self.defender_tactic)
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