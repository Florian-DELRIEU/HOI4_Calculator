from W40K.LandBattles.Tactics.Tactics_class import Tactic

Attack = Tactic(SA=1.05,HA=1.05,CAC=0.1,isDefenseTactic=False,Name="Attaque")
Assaut = Tactic(SA=1.25,HA=1.25,CAC=0.3,isDefenseTactic=False,Name="Assaut")
Shock = Tactic(BRK=1.25,CAC=0.5,isDefenseTactic=False,Name="Shock")

Defense = Tactic(DEF=1.05,isDefenseTactic=True,Name="Defense")
CounterAttack = Tactic(DEF=1.25,CAC=0.1,isDefenseTactic=True,Name="Counter Attack")
TacticWithdrawal = Tactic(DEF=0.95,CAC=-0.3,isDefenseTactic=True,Name="Tactic Withdrawal")