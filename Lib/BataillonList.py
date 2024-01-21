from Class.Bataillon import *

## INFANTERIE
INF_36 = Bataillon(pv=25, org=60, sa=6, ha=1, defense=23.1, attack=3.15, armor=0, prc=4, hard=0, width=2, supply_use=0.07,
                   fuel_use=0, ic=50, name="Infanterie 36")
CAV_36 = Bataillon(pv=25, org=70, sa=6, ha=1, defense=22.44, attack=3.06, armor=0, prc=4, hard=0, width=2, supply_use=0.12,
                   fuel_use=0, ic=60, name="Cavalerie 36")
MOT_36 = Bataillon(pv=25, org=60, sa=6, ha=1, defense=23.1, attack=3.15, armor=0, prc=4, hard=.1, width=2, supply_use=0.11,
                   fuel_use=1.2, ic=175, name="Motorized 36")

## ARTILLERIE
ART_36 = Bataillon(pv=0.6, org=0, sa=27.5, ha=2, defense=10, attack=6, armor=0, prc=5, hard=0, width=3, supply_use=0.2,
                   fuel_use=0, ic=126, name="Artillerie 36")

## ARMOR
LARM_36 = Bataillon(pv=2, org=10, sa=16, ha=6, defense=5, attack=36, armor=15, prc=30, hard=.8, width=2, supply_use=0.2,
                    fuel_use=2.4, ic=540, name="Light Armor 36")
MARM_39 = Bataillon(pv=2, org=10, sa=19, ha=14, defense=5, attack=36, armor=60, prc=61, hard=.9, width=2, supply_use=0.22,
                    fuel_use=3.6, ic=600, name="Medium Armor 36")
HARM_39 = Bataillon(pv=2, org=10, sa=15, ha=12, defense=6, attack=36, armor=70, prc=35, hard=.95, width=2, supply_use=0.3,
                    fuel_use=4.4, ic=1000, name="Heavy Armor 36")

## SUPPORT
S_ART_36 = Bataillon(pv=0.2, org=0, sa=17.5, ha=1.2, defense=6, attack=3.6, armor=0, prc=5, hard=0, width=0, supply_use=0.16,
                     fuel_use=0, ic=42, name="Support Artillerie 36")
