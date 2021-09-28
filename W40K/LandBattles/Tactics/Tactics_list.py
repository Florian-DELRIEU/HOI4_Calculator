from W40K.LandBattles.Tactics.Tactics_class import Tactic

## ATTACKS
ATK_list = [
Tactic(ATK_Damage=1.05,CAC=0,isDefenseTactic=False,Name="Attaque"),
Tactic(ATK_Damage=1.25,CAC=0.5,isDefenseTactic=False,Name="Assaut"),
Tactic(DEF_Damage=0.75,CAC=0.3,isDefenseTactic=False,Name="Shock"),
Tactic(ATK_Damage=1.1,DEF_Damage=0.95,CAC=.1,isDefenseTactic=False,Name="Infiltration Assaut"),
Tactic(ATK_Damage=1.15,DEF_Damage=1,CAC=0,isDefenseTactic=False,Name="Well-Planned Attack"),
Tactic(ATK_Damage=1.20,DEF_Damage=1.05,CAC=0.3,isDefenseTactic=False,Name="Relentless Assault"),
Tactic(ATK_Damage=1.15,DEF_Damage=1,CAC=0.3,isDefenseTactic=False,Name="Unexpected Thrust"),
Tactic(ATK_Damage=1.10,DEF_Damage=0.8,CAC=-.5,isDefenseTactic=False,Name="Suppressive Barrage"),
# Need requirements
Tactic(DEF_Damage=1.05,ATK_Damage=1.25,CAC=0,isDefenseTactic=False,weight=0,Name="Encirclement"),
Tactic(DEF_Damage=0.85,ATK_Damage=1.25,CAC=0.1,isDefenseTactic=False,weight=0,Name="Breakthrough"),
Tactic(DEF_Damage=0.85,ATK_Damage=1.15,CAC=.2,isDefenseTactic=False,weight=0,Name="Blitz"),
Tactic(DEF_Damage=0.95,ATK_Damage=1.2,CAC=.3,isDefenseTactic=False,weight=0,Name="Seize Bridge"),
Tactic(DEF_Damage=1.1,ATK_Damage=1.1,CAC=.5,isDefenseTactic=False,weight=0,Name="Mass Charge"),
]

## DEFENSES
DEF_list = [
Tactic(DEF_Damage=1.05,isDefenseTactic=True,Name="Defense"),
Tactic(DEF_Damage=1.25,CAC=0.3,isDefenseTactic=True,Name="Counter Attack"),
Tactic(ATK_Damage=0.75,DEF_Damage=0.95,CAC=-0.3,isDefenseTactic=True,Name="Tactic Withdrawal"),
Tactic(ATK_Damage=0.75,DEF_Damage=1.15,CAC=-0.1,isDefenseTactic=True,Name="Delay"),
Tactic(ATK_Damage=0.75,DEF_Damage=1,CAC=0.1,isDefenseTactic=True,Name="Ambush"),
Tactic(ATK_Damage=0.85,DEF_Damage=1.1,CAC=-0.3,isDefenseTactic=True,Name="Elastic Defense"),
Tactic(ATK_Damage=0.80,DEF_Damage=1.2,CAC=0.1,isDefenseTactic=True,Name="Backhand Blow"),
Tactic(ATK_Damage=0.3,DEF_Damage=.4,CAC=.5,isDefenseTactic=True,Name="Guerrilla Tactics"),
Tactic(ATK_Damage=0.9,DEF_Damage=1.1,CAC=-0.5,isDefenseTactic=True,Name="Overwhelming Fire"),
# Need Requirement
Tactic(ATK_Damage=1.2,DEF_Damage=.95,CAC=0,isDefenseTactic=True,weight=0,Name="Hold Bridge"),
]


########################################################################################################################
## Close Quarter Attack
ATK_CQ_list = [
Tactic(ATK_Damage=1.1,DEF_Damage=1.05,CAC=0.3,isDefenseTactic=False,weight=0,Name="Close Quarter Attack"),
Tactic(ATK_Damage=1.2,DEF_Damage=1.2,CAC=0.5,isDefenseTactic=False,weight=0,Name="Close Quarter Storm"),
Tactic(ATK_Damage=1.05,DEF_Damage=1.05,CAC=-0.3,isDefenseTactic=False,weight=0,Name="Close Quarter Withdraw"),
]

## Close Quarter Defense
DEF_CQ_list = [
Tactic(ATK_Damage=1.1,DEF_Damage=1.05,isDefenseTactic=True,weight=0,Name="Close Quarter Defense"),
Tactic(ATK_Damage=0.8,DEF_Damage=1,isDefenseTactic=True,weight=0,Name="Close Quarter Local Strongpoint"),
]


########################################################################################################################
## Tactical withdraw Attack
ATK_TW_list = [
Tactic(ATK_Damage=0.75,DEF_Damage=0.9,CAC=0,isDefenseTactic=False,weight=0,Name="Tactical withdraw Attack"),
Tactic(ATK_Damage=0.85,DEF_Damage=0.95,CAC=0.2,isDefenseTactic=False,weight=0,Name="Tactical withdraw Pursuit"),
Tactic(ATK_Damage=0.95,DEF_Damage=0.90,CAC=0.4,isDefenseTactic=False,weight=0,Name="Tactical withdraw Intercept"),
]

## Tactical withdraw Defend
DEF_TW_list = [
Tactic(ATK_Damage=0.7,DEF_Damage=0.95,CAC=-0.3,isDefenseTactic=True,weight=0,Name="Tactical withdraw Withdrawal"),
Tactic(ATK_Damage=0.6,DEF_Damage=0.9,CAC=-0.5,isDefenseTactic=True,weight=0,Name="Tactical withdraw Evade"),
]


########################################################################################################################
## Seize Bridge Attacks
ATK_SB_list = [
Tactic(ATK_Damage=1.2,DEF_Damage=1,CAC=0,isDefenseTactic=False,weight=0,Name="Hold Bridge"),
Tactic(ATK_Damage=1.2,DEF_Damage=0.9,CAC=0,isDefenseTactic=False,weight=0,Name="Defend Bridge"),
]

## Seize Bridge Defend
DEF_SB_list = [
Tactic(ATK_Damage=1,DEF_Damage=0.95,CAC=0.1,isDefenseTactic=True,weight=0,Name="Bridge Assaut"),
Tactic(ATK_Damage=1.25,DEF_Damage=0.9,CAC=0.3,isDefenseTactic=True,weight=0,Name="Bridge Reckless Assaut"),
Tactic(ATK_Damage=1.1,DEF_Damage=0.95,CAC=0.5,isDefenseTactic=True,weight=0,Name="Recapture Bridge"),
]


########################################################################################################################
## Hold Bridge Attacks
ATK_HB_list = [
Tactic(ATK_Damage=1.1,DEF_Damage=1,CAC=0.1,isDefenseTactic=False,weight=0,Name="Attack Bridge"),
Tactic(ATK_Damage=1.2,DEF_Damage=1,CAC=0.3,isDefenseTactic=False,weight=0,Name="Rush Bridge"),
Tactic(ATK_Damage=1.2,DEF_Damage=1.05,CAC=0.5,isDefenseTactic=False,weight=0,Name="Bridge Storm Assaut"),
]

## Hold Bridge Defend
DEF_HB_list = [
Tactic(ATK_Damage=1.2,DEF_Damage=0.9,CAC=0,isDefenseTactic=True,weight=0,Name="Hold Assaut"),
Tactic(ATK_Damage=1.1,DEF_Damage=1.05,CAC=0,isDefenseTactic=True,weight=0,Name="Defend Assaut"),
]
