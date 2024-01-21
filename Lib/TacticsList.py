from Class.Tactics import *
# Tactic(  attacker_damage,  defender_damage,  weight,  counterred_by,  begin_phase,  name )

## ATTACKS
ATK_TACTICS = [
Tactic(attacker_damage=1.05, name="Attaque",
       countered_by="Counter Attack"),
Tactic(attacker_damage=1.25, weight=2, name="Assaut",
       countered_by="Counter Attack",
       begin_phase="Close Quarter Combat"),
Tactic(defender_damage=0.75, name="Shock",
       countered_by="Ambush"),
Tactic(attacker_damage=1.1, defender_damage=0.95, name="Infiltration Assaut"),
Tactic(attacker_damage=1.15, defender_damage=1, name="Well-Planned Attack"),
Tactic(attacker_damage=1.20, defender_damage=1.05, name="Relentless Assault"),
Tactic(attacker_damage=1.15, defender_damage=1, name="Unexpected Thrust"),
Tactic(attacker_damage=1.10, defender_damage=0.8, name="Suppressive Barrage"),
# Need requirements
Tactic(defender_damage=1.05, attacker_damage=1.25, weight=0, name="Encirclement",
       countered_by="Tactical Withdrawal"),
Tactic(defender_damage=0.85, attacker_damage=1.25, weight=0, name="Breakthrough",
       countered_by="Backhand Blow"),
Tactic(defender_damage=0.85, attacker_damage=1.15, weight=0, name="Blitz",
       countered_by="Elastic Defense"),
Tactic(defender_damage=0.95, attacker_damage=1.2, weight=0, name="Seize Bridge",
       begin_phase="Seize Bridge"),
Tactic(defender_damage=1.1, attacker_damage=1.1, weight=0, name="Mass Charge"),
]

## DEFENSES
DEF_TACTICS = [
Tactic(defender_damage=1.05, name="Defense"),
Tactic(defender_damage=1.25, name="Counter Attack"),
Tactic(attacker_damage=0.75, defender_damage=0.95, name="Tactic Withdrawal",
       begin_phase="Tactic Withdraw"),
Tactic(attacker_damage=0.75, defender_damage=1.15, name="Delay",
       countered_by="Shock"),
Tactic(attacker_damage=0.75, defender_damage=1, name="Ambush",
       countered_by="Breakthrough"),
Tactic(attacker_damage=0.85, defender_damage=1.1, name="Elastic Defense"),
Tactic(attacker_damage=0.80, defender_damage=1.2, name="Backhand Blow"),
Tactic(attacker_damage=0.3, defender_damage=.4, name="Guerrilla"),
Tactic(attacker_damage=0.9, defender_damage=1.1, weight=2, name="Overwhelming Fire"),
# Need Requirement
Tactic(attacker_damage=1.2, defender_damage=.95, weight=0, name="Hold Bridge",
       begin_phase="Hold Bridge"),
]


########################################################################################################################
## Close Quarter Attack
ATK_CQ_TACTICS = [
Tactic(attacker_damage=1.1, defender_damage=1.05, name="Close Quarter Attack"),
Tactic(attacker_damage=1.2, defender_damage=1.2, weight=2, name="Close Quarter Storm"),
Tactic(attacker_damage=1.05, defender_damage=1.05, weight=1, name="Close Quarter Withdraw",
       begin_phase="Default"),
]

## Close Quarter Defense
DEF_CQ_TACTICS = [
Tactic(attacker_damage=1.1, defender_damage=1.05, name="Close Quarter Defense"),
Tactic(attacker_damage=0.8, defender_damage=1, weight=2, name="Close Quarter Local Strongpoint"),
]


########################################################################################################################
## Tactical withdraw Attack
ATK_TW_TACTICS = [
Tactic(attacker_damage=0.75, defender_damage=0.9, name="Tactical withdraw Attack"),
Tactic(attacker_damage=0.85, defender_damage=0.95, name="Pursuit"),
Tactic(attacker_damage=0.95, defender_damage=0.90, name="Intercept",
       begin_phase="Default"),
]

## Tactical withdraw Defend
DEF_TW_TACTICS = [
Tactic(attacker_damage=0.7, defender_damage=0.95, name="Withdrawal"),
Tactic(attacker_damage=0.6, defender_damage=0.9, name="Evade"),
]


########################################################################################################################
## Seize Bridge Attacks
ATK_SB_TACTICS = [
Tactic(attacker_damage=1.2, defender_damage=1, name="Hold Bridge"),
Tactic(attacker_damage=1.2, defender_damage=0.9, name="Defend Bridge"),
]

## Seize Bridge Defend
DEF_SB_TACTICS = [
Tactic(attacker_damage=1, defender_damage=0.95, name="Bridge Assaut"),
Tactic(attacker_damage=1.25, defender_damage=0.9, name="Bridge Reckless Assaut"),
Tactic(attacker_damage=1.1, defender_damage=0.95, name="Recapture Bridge",
       countered_by="Defend Bridge",
       begin_phase="Hold Bridge"),
]


########################################################################################################################
## Hold Bridge Attacks
ATK_HB_TACTICS = [
Tactic(attacker_damage=1.1, defender_damage=1, name="Attack Bridge"),
Tactic(attacker_damage=1.2, defender_damage=1, name="Rush Bridge"),
Tactic(attacker_damage=1.2, defender_damage=1.05, weight=2, name="Storm Bridge",
       countered_by="Defend Bridge",
       begin_phase="Seize Bridge"),
]

## Hold Bridge Defend
DEF_HB_TACTICS = [
Tactic(attacker_damage=1.2, defender_damage=0.9, name="Hold Bridge"),
Tactic(attacker_damage=1.1, defender_damage=1.05, name="Defend Bridge"),
]
