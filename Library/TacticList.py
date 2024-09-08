from Classes.Tactics import *
from Functions.TacticTriggersFunctions import *

## ATTACKS
ATK_TACTICS = [
Tactic(attacker_bonus=1.05,
       name="Attack",
       countered_by="Counter Attack"
       ),

Tactic(attacker_bonus=1.25,
       weight=0.4,
       name="Assault",
       countered_by="Counter Attack",
       begin_phase="Close Quarter Combat"
       ),

Tactic(defender_bonus=1.05,
       attacker_bonus=1.25,
       weight=4,
       weight_mult=0,
       width_bonus=1.5,
       name="Encirclement",
       countered_by="Tactical Withdrawal",
       ),

Tactic(defender_bonus=0.75,
       name="Shock",
       weight_mult=0,
       countered_by="Ambush",
       ),

Tactic(defender_bonus=0.85,
       attacker_bonus=1.25,
       weight_mult=0,
       name="Breakthrough",
       countered_by="Backhand Blow"
       ),

Tactic(defender_bonus=0.85,
       attacker_bonus=1.15,
       weight_mult=0,
       name="Blitz",
       countered_by="Elastic Defense"
       ),

Tactic(defender_bonus=0.8,
       attacker_bonus=1.2,
       width_bonus=1.1,
       weight_mult=0,
       name="Masterful Blitz",
       countered_by="Elastic Defense"
       ),

Tactic(defender_bonus=0.95,
       attacker_bonus=1.2,
       weight=2,
       weight_mult=0,
       width_bonus=0.75,
       name="Seize Bridge",
       begin_phase="Seize Bridge"
       ),

Tactic(defender_bonus=1.1,
       attacker_bonus=1.1,
       weight=4,
       weight_mult=0,
       width_bonus=1.5,
       name="Mass Charge"
       ),

Tactic(defender_bonus=1.1,
       attacker_bonus=1.25,
       weight_mult=0,
       name="Banzai Charge",
       countered_by="Overwhelming Fire"
       ),

Tactic(attacker_bonus=1.1,
       defender_bonus=0.95,
       name="Infiltration Assaut"
       ),

Tactic(attacker_bonus=1.15,
       defender_bonus=1,
       name="Well-Planned Attack"
       ),

Tactic(attacker_bonus=1.20,
       defender_bonus=1.05,
       name="Relentless Assault"
       ),

Tactic(attacker_bonus=1.15,
       defender_bonus=1,
       name="Unexpected Thrust"
       ),

Tactic(attacker_bonus=1.10,
       defender_bonus=0.8,
       name="Suppressive Barrage"
       ),
]

## DEFENSES
DEF_TACTICS = [
Tactic(defender_bonus=1.05,
       name="Defend"
       ),

Tactic(defender_bonus=1.25,
       name="Counter-Attack",
       weight_mult=0
       ),

Tactic(attacker_bonus=0.75,
       defender_bonus=1.15,
       name="Delay",
       countered_by="Shock"
       ),

Tactic(attacker_bonus=0.75,
       defender_bonus=0.95,
       width_bonus=0.75,
       name="Tactic Withdrawal",
       begin_phase="Tactic Withdraw"
       ),

Tactic(attacker_bonus=0.75,
       defender_bonus=1,
       name="Ambush",
       countered_by="Breakthrough"
       ),

Tactic(attacker_bonus=0.85,
       defender_bonus=1.1,
       name="Elastic Defense"
       ),

Tactic(attacker_bonus=0.80,
       defender_bonus=1.2,
       name="Backhand Blow"
       ),

Tactic(attacker_bonus=1.2,
       defender_bonus=.95,
       weight=2,
       width_bonus=0.75,
       name="Hold Bridge",
       begin_phase="Hold Bridge"
       ),

Tactic(attacker_bonus=0.3,
       defender_bonus=.4,
       width_bonus=0.5,
       name="Guerrilla Tactics"
       ),

Tactic(attacker_bonus=0.9,
       defender_bonus=1.1,
       weight=2,
       name="Overwhelming Fire"
       ),
]


########################################################################################################################
## Close Quarter Attack
ATK_CQ_TACTICS = [
Tactic(attacker_bonus=1.1,
       defender_bonus=1.05,
       name="Close Quarter Attack"
       ),

Tactic(attacker_bonus=1.2,
       defender_bonus=1.2,
       weight=2,
       name="Close Quarter Storm"
       ),

Tactic(attacker_bonus=1.05,
       defender_bonus=1.05,
       weight=1,
       name="Close Quarter Withdraw",
       begin_phase="Default"
       ),
]

## Close Quarter Defense
DEF_CQ_TACTICS = [
Tactic(attacker_bonus=1.1,
       defender_bonus=1.05,
       name="Close Quarter Defense"
       ),

Tactic(attacker_bonus=0.8,
       defender_bonus=1,
       weight=2,
       name="Close Quarter Local Strongpoint"
       ),
]


########################################################################################################################
## Tactical withdraw Attack
ATK_TW_TACTICS = [
Tactic(attacker_bonus=0.75,
       defender_bonus=0.9,
       width_bonus=0.75,
       name="Tactical withdraw Attack"
       ),

Tactic(attacker_bonus=0.85,
       defender_bonus=0.95,
       width_bonus=0.75,
       name="Pursuit"
       ),

Tactic(attacker_bonus=0.95,
       defender_bonus=0.90,
       name="Intercept",
       begin_phase="Default"
       ),
]

## Tactical withdraw Defend
DEF_TW_TACTICS = [
Tactic(attacker_bonus=0.7,
       defender_bonus=0.95,
       width_bonus=0.75,
       name="Withdrawal"
       ),

Tactic(attacker_bonus=0.6,
       defender_bonus=0.9,
       width_bonus=0.75,
       name="Evade"
       ),
]


########################################################################################################################
## Seize Bridge Attacks
ATK_SB_TACTICS = [
Tactic(attacker_bonus=1.2,
        defender_bonus=1,
        width_bonus=0.75,
        name="Hold Bridge"
       ),

Tactic(attacker_bonus=1.2,
        defender_bonus=0.9,
        width_bonus=0.75,
        name="Defend Bridge"
       ),
]

## Seize Bridge Defend
DEF_SB_TACTICS = [
Tactic(attacker_bonus=1,
        defender_bonus=0.95,
        width_bonus=0.75,
        name="Assault Bridge"
       ),

Tactic(attacker_bonus=1.25,
        defender_bonus=0.9,
        width_bonus=0.75,
        name="Reckless Assaut"
       ),

Tactic(attacker_bonus=1.1,
        defender_bonus=0.95,
        width_bonus=0.75,
        name="Recapture Bridge",
        countered_by="Defend Bridge",
        begin_phase="Hold Bridge"
       ),
]


########################################################################################################################
## Hold Bridge Attacks
ATK_HB_TACTICS = [
Tactic(attacker_bonus=1.1,
       defender_bonus=1,
       width_bonus=0.75,
       name="Attack Bridge"
       ),

Tactic(attacker_bonus=1.2,
       defender_bonus=1,
       width_bonus=0.75,
       name="Rush Bridge"
       ),

Tactic(attacker_bonus=1.2,
       defender_bonus=1.05,
       weight=2,
       width_bonus=0.75,
       name="Storm Bridge",
       countered_by="Defend Bridge",
       begin_phase="Seize Bridge"
       ),
]

## Hold Bridge Defend
DEF_HB_TACTICS = [
Tactic(attacker_bonus=1.2,
       defender_bonus=0.9,
       weight=2,
       width_bonus=0.75,
       name="Hold Bridge"
       ),

Tactic(attacker_bonus=1.1,
       defender_bonus=1.05,
       weight=2,
       width_bonus=0.75,
       name="Defend Bridge"
       ),
]