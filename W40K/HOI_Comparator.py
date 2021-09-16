from DivisionList import *
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
    txt += "\nHP   |   {}    |   {}  (+ {} %)  ".format(DivA._PVmax, DivB._PVmax, 100*(divide(DivB._PVmax, DivA._PVmax) - 1))
    txt += "\nORG  |   {}    |   {}  (+ {} %)  ".format(DivA._ORG, DivB._ORG, 100*(divide(DivB._ORG, DivA._ORG) - 1))
    txt += "\nSA   |   {}    |   {}  (+ {} %)  ".format(DivA.SA, DivB.SA, 100*(divide(DivB.SA, DivA.SA) - 1))
    txt += "\nHA   |   {}    |   {}  (+ {} %)  ".format(DivA.HA, DivB.HA, 100*(divide(DivB.HA, DivA.HA) - 1))
    txt += "\nDEF  |   {}    |   {}  (+ {} %)  ".format(DivA.DEF, DivB.DEF, 100*(divide(DivB.DEF, DivA.DEF) - 1))
    txt += "\nBRK  |   {}    |   {}  (+ {} %)  ".format(DivA.BRK, DivB.BRK, 100*(divide(DivB.BRK,DivA.BRK) - 1))
    txt += "\nARM  |   {}    |   {}  (+ {} %)  ".format(DivA.ARM, DivB.ARM, 100*(divide(DivB.ARM, DivA.ARM) - 1))
    txt += "\nPRC  |   {}    |   {}  (+ {} %)  ".format(DivA.PRC, DivB.PRC, 100*(divide(DivB.PRC, DivA.PRC) - 1))
    txt += "\nHRD  |   {}    |   {}  (+ {} %)  ".format(DivA.HARD, DivB.HARD, 100*(divide(DivB.HARD, DivA.HARD) - 1))

    txt +="\n \n"
    print(txt)


##### TESTING
Analyse_Division(Infantery_72)
Analyse_Division(Armored_432)

Compare_Division(Infantery_72,Armored_432)