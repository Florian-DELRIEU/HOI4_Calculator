from W40K.LandBattles.Tactics.Tactics_class import Tactic

## ATTACKS
Attack = Tactic(ATK_Damage=1.05,CAC=0,isDefenseTactic=False,Name="Attaque")
Assaut = Tactic(ATK_Damage=1.25,CAC=0.5,isDefenseTactic=False,Name="Assaut")
Shock = Tactic(DEF_Damage=0.75,CAC=0.3,isDefenseTactic=False,Name="Shock")
Infiltration_Assault = Tactic(ATK_Damage=1.1,DEF_Damage=0.95,CAC=.1,isDefenseTactic=False,Name="Infiltration Assaut")
Well_Planned_Attack = Tactic(ATK_Damage=1.15,DEF_Damage=1,CAC=0,isDefenseTactic=False,Name="Well-Planned Attack")
Relentless_Assault = Tactic(ATK_Damage=1.20,DEF_Damage=1.05,CAC=0.3,isDefenseTactic=False,Name="Relentless Assault")
Unexpected_Thrust = Tactic(ATK_Damage=1.15,DEF_Damage=1,CAC=0.3,isDefenseTactic=False,Name="Unexpected Thrust")
Suppressive_Barrage = Tactic(ATK_Damage=1.10,DEF_Damage=0.8,CAC=-.5,isDefenseTactic=False,Name="Suppressive Barrage")
# Need requirements
Encirclement = Tactic(DEF_Damage=1.05,ATK_Damage=1.25,CAC=0,isDefenseTactic=False,weight=0,Name="Encirclement")
Breakthrough = Tactic(DEF_Damage=0.85,ATK_Damage=1.25,CAC=0.1,isDefenseTactic=False,weight=0,Name="Breakthrough")
Blitz = Tactic(DEF_Damage=0.85,ATK_Damage=1.15,CAC=.2,isDefenseTactic=False,weight=0,Name="Blitz")
Seize_Bridge = Tactic(DEF_Damage=0.95,ATK_Damage=1.2,CAC=.3,isDefenseTactic=False,weight=0,Name="Seize Bridge")
Mass_Charge = Tactic(DEF_Damage=1.1,ATK_Damage=1.1,CAC=.5,isDefenseTactic=False,weight=0,Name="Mass Charge")

## DEFENSES
Defense = Tactic(DEF_Damage=1.05,isDefenseTactic=True,Name="Defense")
CounterAttack = Tactic(DEF_Damage=1.25,CAC=0.3,isDefenseTactic=True,Name="Counter Attack")
TacticWithdrawal = Tactic(ATK_Damage=0.75,DEF_Damage=0.95,CAC=-0.3,isDefenseTactic=True,Name="Tactic Withdrawal")
Delay = Tactic(ATK_Damage=0.75,DEF_Damage=1.15,CAC=-0.1,isDefenseTactic=True,Name="Delay")
Ambush = Tactic(ATK_Damage=0.75,DEF_Damage=1,CAC=0.1,isDefenseTactic=True,Name="Ambush")
Elastic_Defense = Tactic(ATK_Damage=0.85,DEF_Damage=1.1,CAC=-0.3,isDefenseTactic=True,Name="Elastic Defense")
Backhand_Blow = Tactic(ATK_Damage=0.80,DEF_Damage=1.2,CAC=0.1,isDefenseTactic=True,Name="Backhand Blow")
Guerrilla_Tactics = Tactic(ATK_Damage=0.3,DEF_Damage=.4,CAC=.5,isDefenseTactic=True,Name="Guerrilla Tactics")
Overwhelming_Fire = Tactic(ATK_Damage=0.9,DEF_Damage=1.1,CAC=-0.5,isDefenseTactic=True,Name="Overwhelming Fire")
# Need Requirement
Hold_Bridge = Tactic(ATK_Damage=1.2,DEF_Damage=.95,CAC=0,isDefenseTactic=True,weight=0,Name="Hold Bridge")


########################################################################################################################
## Close Quarter Attack
CQ_Attack = Tactic(ATK_Damage=1.1,DEF_Damage=1.05,CAC=0.3,isDefenseTactic=False,weight=0,Name="Close Quarter Attack")
CQ_Storm = Tactic(ATK_Damage=1.2,DEF_Damage=1.2,CAC=0.5,isDefenseTactic=False,weight=0,Name="Close Quarter Storm")
CQ_Withdraw = Tactic(ATK_Damage=1.05,DEF_Damage=1.05,CAC=-0.3,isDefenseTactic=False,weight=0,Name="Close Quarter Withdraw")

## Close Quarter Defense
CQ_Defense = Tactic(ATK_Damage=1.1,DEF_Damage=1.05,isDefenseTactic=True,weight=0,Name="Close Quarter Defense")
CQ_Local_Strongpoint = Tactic(ATK_Damage=0.8,DEF_Damage=1,isDefenseTactic=True,weight=0,Name="Close Quarter Local Strongpoint")


########################################################################################################################
## Tactical withdraw Attack
TW_Attack = Tactic(ATK_Damage=0.75,DEF_Damage=0.9,CAC=0,isDefenseTactic=False,weight=0,Name="Tactical withdraw Attack")
TW_Pursuit = Tactic(ATK_Damage=0.85,DEF_Damage=0.95,CAC=0.2,isDefenseTactic=False,weight=0,Name="Tactical withdraw Pursuit")
TW_Intercept = Tactic(ATK_Damage=0.95,DEF_Damage=0.90,CAC=0.4,isDefenseTactic=False,weight=0,Name="Tactical withdraw Intercept")

## Tactical withdraw Defend
TW_Withdrawal = Tactic(ATK_Damage=0.7,DEF_Damage=0.95,CAC=-0.3,isDefenseTactic=True,weight=0,Name="Tactical withdraw Withdrawal")
TW_Evade = Tactic(ATK_Damage=0.6,DEF_Damage=0.9,CAC=-0.5,isDefenseTactic=True,weight=0,Name="Tactical withdraw Evade")


########################################################################################################################
## Seize Bridge Attacks
SB_Hold = Tactic(ATK_Damage=1.2,DEF_Damage=1,CAC=0,isDefenseTactic=False,weight=0,Name="Hold Bridge")
SB_Defend = Tactic(ATK_Damage=1.2,DEF_Damage=0.9,CAC=0,isDefenseTactic=False,weight=0,Name="Defend Bridge")

## Seize Bridge Defend
SB_Assaut = Tactic(ATK_Damage=1,DEF_Damage=0.95,CAC=0.1,isDefenseTactic=True,weight=0,Name="Bridge Assaut")
SB_Reckless_Assaut = Tactic(ATK_Damage=1.25,DEF_Damage=0.9,CAC=0.3,isDefenseTactic=True,weight=0,Name="Bridge Reckless Assaut")
SB_Recapture_Bridge = Tactic(ATK_Damage=1.1,DEF_Damage=0.95,CAC=0.5,isDefenseTactic=True,weight=0,Name="Recapture Bridge")


########################################################################################################################
## Hold Bridge Attacks
HB_Attack = Tactic(ATK_Damage=1.1,DEF_Damage=1,CAC=0.1,isDefenseTactic=False,weight=0,Name="Attack Bridge")
HB_Rush = Tactic(ATK_Damage=1.2,DEF_Damage=1,CAC=0.3,isDefenseTactic=False,weight=0,Name="Rush Bridge")
HB_Storm = Tactic(ATK_Damage=1.2,DEF_Damage=1.05,CAC=0.5,isDefenseTactic=False,weight=0,Name="Bridge Storm Assaut")

## Hold Bridge Defend
HB_Hold = Tactic(ATK_Damage=1.2,DEF_Damage=0.9,CAC=0,isDefenseTactic=True,weight=0,Name="Hold Assaut")
HB_Defend = Tactic(ATK_Damage=1.1,DEF_Damage=1.05,CAC=0,isDefenseTactic=True,weight=0,Name="Defend Assaut")