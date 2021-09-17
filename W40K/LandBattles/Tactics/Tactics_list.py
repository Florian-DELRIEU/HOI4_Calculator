from W40K.LandBattles.Tactics.Tactics_class import Tactic

## ATTACKS
Attack = Tactic(ATK_Damage=1.05,CAC=0,isDefenseTactic=False,Name="Attaque")
Assaut = Tactic(ATK_Damage=1.25,CAC=0.5,isDefenseTactic=False,Name="Assaut")
Shock = Tactic(DEF_Damage=0.75,CAC=0.3,isDefenseTactic=False,Name="Shock")

## DEFENSES
Defense = Tactic(DEF_Damage=1.05,isDefenseTactic=True,Name="Defense")
CounterAttack = Tactic(DEF_Damage=1.25,CAC=0.3,isDefenseTactic=True,Name="Counter Attack")
TacticWithdrawal = Tactic(ATK_Damage=0.75,DEF_Damage=0.95,CAC=-0.3,isDefenseTactic=True,Name="Tactic Withdrawal")

## Close Quarter Attack
CloseQuarterAttack = Tactic(ATK_Damage=1.1,DEF_Damage=1.05,CAC=0.3,isDefenseTactic=False,
                            weight=0,Name="Close Quarter Attack")