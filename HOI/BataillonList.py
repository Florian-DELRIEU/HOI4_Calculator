from HOI.Class import Bataillon


## INFANTERIE
INF_36 = Bataillon(PV=25,ORG=60,SA=6,HA=1,DEF=23.1,BRK=3.15,ARM=0,PRC=4,HARD=0,Width=2,Supply_use=0.07,
                   Fuel_use=0,IC=50,Name="Infanterie 36")
CAV_36 = Bataillon(PV=25,ORG=70,SA=6,HA=1,DEF=22.44,BRK=3.06,ARM=0,PRC=4,HARD=0,Width=2,Supply_use=0.12,
                   Fuel_use=0,IC=60,Name="Cavalerie 36")
MOT_36 = Bataillon(PV=25, ORG=60, SA=6, HA=1, DEF=23.1, BRK=3.15, ARM=0, PRC=4, HARD=.1, Width=2, Supply_use=0.11,
                   Fuel_use=1.2,IC=175, Name="Motorized 36")

## ARTILLERIE
ART_36 = Bataillon(PV=0.6, ORG=0, SA=27.5, HA=2, DEF=10, BRK=6, ARM=0, PRC=5, HARD=0, Width=3, Supply_use=0.2,
                   Fuel_use=0,IC=126, Name="Artillerie 36")

## ARMOR
LARM_36 = Bataillon(PV=2,ORG=10,SA=16,HA=6,DEF=5,BRK=36,ARM=15,PRC=30,HARD=.8,Width=2,Supply_use=0.2,
                    Fuel_use=2.4,IC=540,Name="Light Armor 36")
MARM_39 = Bataillon(PV=2,ORG=10,SA=19,HA=14,DEF=5,BRK=36,ARM=60,PRC=61,HARD=.9,Width=2,Supply_use=0.22,
                    Fuel_use=3.6,IC=600,Name="Medium Armor 36")
HARM_39 = Bataillon(PV=2,ORG=10,SA=15,HA=12,DEF=6,BRK=36,ARM=70,PRC=35,HARD=.95,Width=2,Supply_use=0.3,
                    Fuel_use=4.4,IC=1000,Name="Heavy Armor 36")

## SUPPORT
S_ART_36 = Bataillon(PV=0.2, ORG=0, SA=17.5, HA=1.2, DEF=6, BRK=3.6, ARM=0, PRC=5, HARD=0, Width=0, Supply_use=0.16,
                   Fuel_use=0,IC=42, Name="Support Artillerie 36")