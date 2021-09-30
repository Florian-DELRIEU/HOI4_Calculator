from W40K.LandBattles.Tactics.Tactics_class import Tactic

## ATTACKS
ATK_tactics = [
Tactic(ATK_Damage=1.05,CAC=0,Name="Attaque",
    CounteredBy="Counter Attack"),
Tactic(ATK_Damage=1.25,CAC=0.5,weight=2,Name="Assaut",
        CounteredBy="Counter Attack",
        BeginPhase="Close Quarter Combat"),
Tactic(DEF_Damage=0.75,CAC=0.3,Name="Shock",
       CounteredBy="Ambush"),
Tactic(ATK_Damage=1.1,DEF_Damage=0.95,CAC=.1,Name="Infiltration Assaut"),
Tactic(ATK_Damage=1.15,DEF_Damage=1,CAC=0,Name="Well-Planned Attack"),
Tactic(ATK_Damage=1.20,DEF_Damage=1.05,CAC=0.3,Name="Relentless Assault"),
Tactic(ATK_Damage=1.15,DEF_Damage=1,CAC=0.3,Name="Unexpected Thrust"),
Tactic(ATK_Damage=1.10,DEF_Damage=0.8,CAC=-.5,Name="Suppressive Barrage"),
# Need requirements
Tactic(DEF_Damage=1.05,ATK_Damage=1.25,CAC=0,weight=0,Name="Encirclement",
       CounteredBy="Tactical Withdrawal"),
Tactic(DEF_Damage=0.85,ATK_Damage=1.25,CAC=0.1,weight=0,Name="Breakthrough",
       CounteredBy="Backhand Blow"),
Tactic(DEF_Damage=0.85,ATK_Damage=1.15,CAC=.2,weight=0,Name="Blitz",
       CounteredBy="Elastic Defense"),
Tactic(DEF_Damage=0.95,ATK_Damage=1.2,CAC=.3,weight=0,Name="Seize Bridge",
       BeginPhase="Seize Bridge"),
Tactic(DEF_Damage=1.1,ATK_Damage=1.1,CAC=.5,weight=0,Name="Mass Charge"),
]

## DEFENSES
DEF_tactics = [
Tactic(DEF_Damage=1.05,Name="Defense"),
Tactic(DEF_Damage=1.25,CAC=0.3,Name="Counter Attack"),
Tactic(ATK_Damage=0.75,DEF_Damage=0.95,CAC=-0.3,Name="Tactic Withdrawal",
       BeginPhase="Tactic Withdraw"),
Tactic(ATK_Damage=0.75,DEF_Damage=1.15,CAC=-0.1,Name="Delay",
       CounteredBy="Shock"),
Tactic(ATK_Damage=0.75,DEF_Damage=1,CAC=0.1,Name="Ambush",
       CounteredBy="Breakthrough"),
Tactic(ATK_Damage=0.85,DEF_Damage=1.1,CAC=-0.3,Name="Elastic Defense"),
Tactic(ATK_Damage=0.80,DEF_Damage=1.2,CAC=0.3,Name="Backhand Blow"),
Tactic(ATK_Damage=0.3,DEF_Damage=.4,CAC=.1,Name="Guerrilla"),
Tactic(ATK_Damage=0.9,DEF_Damage=1.1,CAC=-0.5,weight=2,Name="Overwhelming Fire"),
# Need Requirement
Tactic(ATK_Damage=1.2,DEF_Damage=.95,CAC=0,weight=0,Name="Hold Bridge",
       BeginPhase="Hold Bridge"),
]


########################################################################################################################
## Close Quarter Attack
ATK_CQ_tactics = [
Tactic(ATK_Damage=1.1,DEF_Damage=1.05,CAC=0.3,Name="Close Quarter Attack"),
Tactic(ATK_Damage=1.2,DEF_Damage=1.2,weight=2,CAC=0.5,Name="Close Quarter Storm"),
Tactic(ATK_Damage=1.05,DEF_Damage=1.05,weight=1,CAC=-0.3,Name="Close Quarter Withdraw",
       BeginPhase="Default"),
]

## Close Quarter Defense
DEF_CQ_tactics = [
Tactic(ATK_Damage=1.1,DEF_Damage=1.05,Name="Close Quarter Defense"),
Tactic(ATK_Damage=0.8,DEF_Damage=1,weight=2,Name="Close Quarter Local Strongpoint"),
]


########################################################################################################################
## Tactical withdraw Attack
ATK_TW_tactics = [
Tactic(ATK_Damage=0.75,DEF_Damage=0.9,CAC=0,Name="Tactical withdraw Attack"),
Tactic(ATK_Damage=0.85,DEF_Damage=0.95,CAC=0.2,Name="Pursuit"),
Tactic(ATK_Damage=0.95,DEF_Damage=0.90,CAC=0.4,Name="Intercept",
       BeginPhase="Default"),
]

## Tactical withdraw Defend
DEF_TW_tactics = [
Tactic(ATK_Damage=0.7,DEF_Damage=0.95,CAC=-0.3,Name="Withdrawal"),
Tactic(ATK_Damage=0.6,DEF_Damage=0.9,CAC=-0.5,Name="Evade"),
]


########################################################################################################################
## Seize Bridge Attacks
ATK_SB_tactics = [
Tactic(ATK_Damage=1.2,DEF_Damage=1,CAC=0,Name="Hold Bridge"),
Tactic(ATK_Damage=1.2,DEF_Damage=0.9,CAC=0,Name="Defend Bridge"),
]

## Seize Bridge Defend
DEF_SB_tactics = [
Tactic(ATK_Damage=1,DEF_Damage=0.95,CAC=0.1,Name="Bridge Assaut"),
Tactic(ATK_Damage=1.25,DEF_Damage=0.9,CAC=0.3,Name="Bridge Reckless Assaut"),
Tactic(ATK_Damage=1.1,DEF_Damage=0.95,CAC=0.5,Name="Recapture Bridge",
       CounteredBy="Defend Bridge",
       BeginPhase="Hold Bridge"),
]


########################################################################################################################
## Hold Bridge Attacks
ATK_HB_tactics = [
Tactic(ATK_Damage=1.1,DEF_Damage=1,CAC=0.1,Name="Attack Bridge"),
Tactic(ATK_Damage=1.2,DEF_Damage=1,CAC=0.3,Name="Rush Bridge"),
Tactic(ATK_Damage=1.2,DEF_Damage=1.05,CAC=0.5,weight=2,Name="Storm Bridge",
       CounteredBy="Defend Bridge",
       BeginPhase="Seize Bridge"),
]

## Hold Bridge Defend
DEF_HB_tactics = [
Tactic(ATK_Damage=1.2,DEF_Damage=0.9,CAC=0,Name="Hold Bridge"),
Tactic(ATK_Damage=1.1,DEF_Damage=1.05,CAC=0,Name="Defend Bridge"),
]
