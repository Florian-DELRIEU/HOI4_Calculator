class Tactic:
    def __init__(self, attacker_bonus=1, defender_bonus=1, width_bonus = 1,
                 countered_by=None, begin_phase=None, name="", weight=4, weight_mult = 1):
        """
        Classe des tactiques
        :param attacker_bonus: Bonus de dommage à l'attaquant
        :param defender_bonus: Bonus de dommage au défenseur
        :param width_bonus: Bonus appliqué à la largeur de bataille
        :param countered_by: Tactique qui contre celle ci
        :param begin_phase: Phase de bataille commencé avec cette tactique
        :param name: Nom de la tactique
        :param weight: Poids pour la sélection #todo pouvoir modifier la valeur des poids
        #todo :param trigger: Condition pour débloquer la tactique
        """
        self.name = name
        self.countered_by = countered_by
        # Bonus
        self.attacker_bonus = attacker_bonus
        self.defender_bonus = defender_bonus
        self.width_bonus    = width_bonus
        # Begin battle phase
        self.weight = weight
        self.begin_battle_phase = begin_phase
        # Trigger
        self.weight_mult = weight_mult

    def __repr__(self):
        return self.name


class BattlePhase(enumerate):
    DEFAULT = "Default"
    CLOSE_QUARTER_COMBAT = "Close Quarter Combat"
    SEIZE_BRIDGE = "Seize Bridge"
    HOLD_BRIDGE = "Hold Bridge"
    TACTICAL_WITHDRAW = "Tactical Withdraw"