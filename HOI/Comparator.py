from DivisionList import *
from BataillonList import *
from MyPack.Math import divide

def Analyse_Division(Division):
    Div = Division
    txt = "Analyzer"
    txt +="\n======= {} ========".format(Division.name)
    txt += "\n HA/SA = {} % ".format(divide(Div.ha, Div.sa)*100)
#    txt += "\n - SA: {} /IC || {}/Width ".format(divide(Div.SA,Div.IC),divide(Div.SA,Div.Width))
#    txt += "\n - HA: {} /IC || {}/Width ".format(divide(Div.HA,Div.IC),divide(Div.HA,Div.Width))
#    txt += "\n - {} SA/Supply || {} HA/Supply ".format(divide(Div.SA,Div.Supply_use),divide(Div.HA,Div.Supply_use))
#    txt += "\n - {} SA/Fuel || {} HA/Fuel ".format(divide(Div.SA,Div.Fuel_use),divide(Div.HA,Div.Fuel_use))
    txt += "\n BRK/DEF = {} ".format(divide(Div.attack, Div.defense))
#    txt += "\n - DEF: {} /IC || {}/Width ".format(divide(Div.DEF,Div.IC),divide(Div.DEF,Div.Width))
#    txt += "\n - BRK: {} /IC || {}/Width ".format(divide(Div.BRK,Div.IC),divide(Div.BRK,Div.Width))
#    txt += "\n - {} DEF/Supply || {} BRK/Supply ".format(divide(Div.DEF,Div.Supply_use),divide(Div.BRK,Div.Supply_use))
#    txt += "\n - {} DEF/Fuel || {} BRK/Fuel ".format(divide(Div.DEF,Div.Fuel_use),divide(Div.BRK,Div.Fuel_use))
    print(txt)

def Compare_Division(DivA, DivB):
    txt = "COMPARATOR"
    txt += "\n========= {}  Vs {} =========".format(DivA.name, DivB.name)
    txt += "\nHP   |   {}    |   {}  (+ {} %)  ".format(DivA.pv, DivB.pv, 100*(divide(DivB.pv, DivA.pv) - 1))
    txt += "\nORG  |   {}    |   {}  (+ {} %)  ".format(DivA.org, DivB.org, 100*(divide(DivB.org, DivA.org) - 1))
    txt += "\nSA   |   {}    |   {}  (+ {} %)  ".format(DivA.sa, DivB.sa, 100*(divide(DivB.sa, DivA.sa) - 1))
    txt += "\nHA   |   {}    |   {}  (+ {} %)  ".format(DivA.ha, DivB.ha, 100*(divide(DivB.ha, DivA.ha) - 1))
    txt += "\nDEF  |   {}    |   {}  (+ {} %)  ".format(DivA.defense, DivB.defense, 100*(divide(DivB.defense, DivA.defense) - 1))
    txt += "\nBRK  |   {}    |   {}  (+ {} %)  ".format(DivA.attack, DivB.attack, 100*(divide(DivB.attack, DivA.attack) - 1))
    txt += "\nARM  |   {}    |   {}  (+ {} %)  ".format(DivA.arm, DivB.arm, 100*(divide(DivB.arm, DivA.arm) - 1))
    txt += "\nPRC  |   {}    |   {}  (+ {} %)  ".format(DivA.prc, DivB.prc, 100*(divide(DivB.prc, DivA.prc) - 1))
    txt += "\nHRD  |   {}    |   {}  (+ {} %)  ".format(DivA.hard, DivB.hard, 100*(divide(DivB.hard, DivA.hard) - 1))
#    txt += "\nIC   |   {}    |   {}  (+ {} %)  ".format(DivA.IC, DivB.IC, 100*(divide(DivB.IC, DivA.IC) - 1))
#    txt += "\nSupply   |   {}    |   {}  (+ {} %)  ".format(DivA.Supply_use, DivB.Supply_use,
#                                                            100*(divide(DivB.Supply_use, DivA.Supply_use) - 1))
#    txt += "\nFuel   |   {}    |   {}  (+ {} %)  ".format(DivA.Fuel_use, DivB.Fuel_use,
#                                                            100*(divide(DivB.Fuel_use, DivA.Fuel_use) - 1))
    txt +="\n \n"
    print(txt)

def Analyze_Bataillon(Bataillon):
    Bat = Bataillon
    txt = "Analyzer"
    txt += "\n======= {} ========".format(Bataillon.name)
    txt += "\n HA/SA = {} % ".format(divide(Bat.ha, Bat.sa)*100)
    txt += "\n - SA: {} /IC || {}/Width ".format(divide(Bat.sa, Bat.IC), divide(Bat.sa, Bat.Width))
    txt += "\n - HA: {} /IC || {}/Width ".format(divide(Bat.ha, Bat.IC), divide(Bat.ha, Bat.Width))
    txt += "\n - {} SA/Supply || {} HA/Supply ".format(divide(Bat.sa, Bat.Supply_use), divide(Bat.ha, Bat.Supply_use))
    txt += "\n - {} SA/Fuel || {} HA/Fuel ".format(divide(Bat.sa, Bat.Fuel_use), divide(Bat.ha, Bat.Fuel_use))
    txt += "\n BRK/DEF = {} ".format(divide(Bat.attack, Bat.defense))
    txt += "\n - DEF: {} /IC || {}/Width ".format(divide(Bat.defense, Bat.IC), divide(Bat.defense, Bat.Width))
    txt += "\n - BRK: {} /IC || {}/Width ".format(divide(Bat.attack, Bat.IC), divide(Bat.attack, Bat.Width))
    txt += "\n - {} DEF/Supply || {} BRK/Supply ".format(divide(Bat.defense, Bat.Supply_use), divide(Bat.attack, Bat.Supply_use))
    txt += "\n - {} DEF/Fuel || {} BRK/Fuel ".format(divide(Bat.defense, Bat.Fuel_use), divide(Bat.attack, Bat.Fuel_use))
    txt += "\n \n"
    print(txt)

def Compare_Bataillon(BatA, BatB):
    txt = "COMPARATOR"
    txt += "\n========= {}  Vs {} =========".format(BatA.name, BatB.name)
    txt += "\nHP   |   {}    |   {}  (+ {} %)  ".format(BatA.pv, BatB.pv, 100*(divide(BatB.pv, BatA.pv) - 1))
    txt += "\nORG  |   {}    |   {}  (+ {} %)  ".format(BatA.org, BatB.org, 100*(divide(BatB.org, BatA.org) - 1))
    txt += "\nSA   |   {}    |   {}  (+ {} %)  ".format(BatA.sa, BatB.sa, 100*(divide(BatB.sa, BatA.sa) - 1))
    txt += "\nHA   |   {}    |   {}  (+ {} %)  ".format(BatA.ha, BatB.ha, 100*(divide(BatB.ha, BatA.ha) - 1))
    txt += "\nDEF  |   {}    |   {}  (+ {} %)  ".format(BatA.defense, BatB.defense, 100*(divide(BatB.defense, BatA.defense) - 1))
    txt += "\nBRK  |   {}    |   {}  (+ {} %)  ".format(BatA.attack, BatB.attack, 100*(divide(BatB.attack, BatA.attack) - 1))
    txt += "\nARM  |   {}    |   {}  (+ {} %)  ".format(BatA.arm, BatB.arm, 100*(divide(BatB.arm, BatA.arm) - 1))
    txt += "\nPRC  |   {}    |   {}  (+ {} %)  ".format(BatA.prc, BatB.prc, 100*(divide(BatB.prc, BatA.prc) - 1))
    txt += "\nHRD  |   {}    |   {}  (+ {} %)  ".format(BatA.hard, BatB.hard, 100*(divide(BatB.hard, BatA.hard) - 1))
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

Analyze_Bataillon(ART_36)
Analyze_Bataillon(S_ART_36)
Compare_Bataillon(ART_36, S_ART_36)