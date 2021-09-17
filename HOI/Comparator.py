from DivisionList import *
from BataillonList import *
from MyPack.Math import divide

def Analyse_Division(Division):
    Div = Division
    txt = "Analyzer"
    txt +="\n======= {} ========".format(Division.Name)
    txt +="\n HA/SA = {} % ".format(divide(Div.HA,Div.SA)*100)
    txt +="\n BRK/DEF = {} ".format(divide(Div.BRK,Div.DEF))
    txt += "\n \n"
    print(txt)

def Compare_Division(DivA, DivB):
    txt = "COMPARATOR"
    txt += "=================="
    txt += "\nHP   |   {}    |   {}  (+ {} %)  ".format(DivA.PV, DivB.PV, 100*(divide(DivB.PV, DivA.PV) - 1))
    txt += "\nORG  |   {}    |   {}  (+ {} %)  ".format(DivA.ORG, DivB.ORG, 100*(divide(DivB.ORG, DivA.ORG) - 1))
    txt += "\nSA   |   {}    |   {}  (+ {} %)  ".format(DivA.SA, DivB.SA, 100*(divide(DivB.SA, DivA.SA) - 1))
    txt += "\nHA   |   {}    |   {}  (+ {} %)  ".format(DivA.HA, DivB.HA, 100*(divide(DivB.HA, DivA.HA) - 1))
    txt += "\nDEF  |   {}    |   {}  (+ {} %)  ".format(DivA.DEF, DivB.DEF, 100*(divide(DivB.DEF, DivA.DEF) - 1))
    txt += "\nBRK  |   {}    |   {}  (+ {} %)  ".format(DivA.BRK, DivB.BRK, 100*(divide(DivB.BRK,DivA.BRK) - 1))
    txt += "\nARM  |   {}    |   {}  (+ {} %)  ".format(DivA.ARM, DivB.ARM, 100*(divide(DivB.ARM, DivA.ARM) - 1))
    txt += "\nPRC  |   {}    |   {}  (+ {} %)  ".format(DivA.PRC, DivB.PRC, 100*(divide(DivB.PRC, DivA.PRC) - 1))
    txt += "\nHRD  |   {}    |   {}  (+ {} %)  ".format(DivA.HARD, DivB.HARD, 100*(divide(DivB.HARD, DivA.HARD) - 1))

    txt +="\n \n"
    print(txt)

def Analyze_Bataillon(Bataillon):
    Bat = Bataillon
    txt = "Analyzer"
    txt += "\n======= {} ========".format(Bataillon.Name)
    txt += "\n HA/SA = {} % ".format(divide(Bat.HA, Bat.SA)*100)
    txt += "\n - SA: {} /IC || {}/Width ".format(divide(Bat.SA,Bat.IC),divide(Bat.SA,Bat.Width))
    txt += "\n - HA: {} /IC || {}/Width ".format(divide(Bat.HA,Bat.IC),divide(Bat.HA,Bat.Width))
    txt += "\n BRK/DEF = {} ".format(divide(Bat.BRK, Bat.DEF))
    txt += "\n - DEF: {} /IC || {}/Width ".format(divide(Bat.DEF,Bat.IC),divide(Bat.DEF,Bat.Width))
    txt += "\n - BRK: {} /IC || {}/Width ".format(divide(Bat.BRK,Bat.IC),divide(Bat.BRK,Bat.Width))
    txt += "\n \n"
    print(txt)

def Compare_Bataillon(BatA, BatB):
    txt = "COMPARATOR"
    txt += "=================="
    txt += "\nHP   |   {}    |   {}  (+ {} %)  ".format(BatA.PV, BatB.PV, 100*(divide(BatB.PV, BatA.PV) - 1))
    txt += "\nORG  |   {}    |   {}  (+ {} %)  ".format(BatA.ORG, BatB.ORG, 100*(divide(BatB.ORG, BatA.ORG) - 1))
    txt += "\nSA   |   {}    |   {}  (+ {} %)  ".format(BatA.SA, BatB.SA, 100*(divide(BatB.SA, BatA.SA) - 1))
    txt += "\nHA   |   {}    |   {}  (+ {} %)  ".format(BatA.HA, BatB.HA, 100*(divide(BatB.HA, BatA.HA) - 1))
    txt += "\nDEF  |   {}    |   {}  (+ {} %)  ".format(BatA.DEF, BatB.DEF, 100*(divide(BatB.DEF, BatA.DEF) - 1))
    txt += "\nBRK  |   {}    |   {}  (+ {} %)  ".format(BatA.BRK, BatB.BRK, 100*(divide(BatB.BRK, BatA.BRK) - 1))
    txt += "\nARM  |   {}    |   {}  (+ {} %)  ".format(BatA.ARM, BatB.ARM, 100*(divide(BatB.ARM, BatA.ARM) - 1))
    txt += "\nPRC  |   {}    |   {}  (+ {} %)  ".format(BatA.PRC, BatB.PRC, 100*(divide(BatB.PRC, BatA.PRC) - 1))
    txt += "\nHRD  |   {}    |   {}  (+ {} %)  ".format(BatA.HARD, BatB.HARD, 100*(divide(BatB.HARD, BatA.HARD) - 1))
    txt += "\nIC   |   {}    |   {}  (+ {} %)  ".format(BatA.IC, BatB.IC, 100*(divide(BatB.IC, BatA.IC) - 1))
    txt += "\nSupply   |   {}    |   {}  (+ {} %)  ".format(BatA.Supply_use, BatB.Supply_use,
                                                            100*(divide(BatB.Supply_use, BatA.Supply_use) - 1))
    txt += "\nFuel   |   {}    |   {}  (+ {} %)  ".format(BatA.Fuel_use, BatB.Fuel_use,
                                                            100*(divide(BatB.Fuel_use, BatA.Fuel_use) - 1))

    txt +="\n \n"
    print(txt)

##### TESTING
Analyse_Division(Infantery_72)
Analyse_Division(Armored_432)

Compare_Division(Infantery_72,Armored_432)

Analyze_Bataillon(CAV_36)
Analyze_Bataillon(M_INF_36)
Compare_Bataillon(CAV_36,M_INF_36)