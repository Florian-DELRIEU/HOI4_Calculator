from Class.Tactics import *

counter_attack = Tactic(defender_damage=1.25,name="Counter Attack")
basic_attack = Tactic(attacker_damage=1.05,name="Attaque",countered_by=counter_attack)