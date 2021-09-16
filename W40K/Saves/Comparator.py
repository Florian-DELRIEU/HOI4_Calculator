from MyPack.Convert import Csv2Dict
from MyPack.Math import divide
from W40K.LandBattles.Company import Company

def Extract_Company(Comp_name=str()):
    DATA = Csv2Dict("SaveCompanies.csv")
    assert Comp_name in DATA.keys() ; "Companies not found in CSV file"
    Comp_name = DATA[Comp_name]
    Comp = Company()
    # Company A
    Comp.HP =  Comp_name[0]
    Comp.ORG = Comp_name[1]
    Comp.SoftAttack = Comp_name[2]
    Comp.HardAttack = Comp_name[3]
    Comp.SoftMeleeAttack = Comp_name[4]
    Comp.HardMeleeAttack = Comp_name[5]
    Comp.Defense = Comp_name[6]
    Comp.Breakthrought = Comp_name[7]
    Comp.Armor = Comp_name[8]
    Comp.Piercing = Comp_name[9]
    Comp.Hardness = Comp_name[10]
    return Comp


def Compare_Company(A=str(),B=str()):
    A = Extract_Company(A)
    B = Extract_Company(B)
    txt = "COMPARATOR"
    txt += "=================="
    txt += "\nHP   |   {}    |   {}  (+ {} %)  ".format(A.HP,B.HP,100*(divide(B.HP,A.HP)-1))
    txt += "\nORG  |   {}    |   {}  (+ {} %)  ".format(A.ORG,B.ORG,100*(divide(B.ORG,A.ORG)-1))
    txt += "\nSA   |   {}    |   {}  (+ {} %)  ".format(A.SoftAttack,B.SoftAttack,100*(divide(B.SoftAttack,A.SoftAttack)-1))
    txt += "\nHA   |   {}    |   {}  (+ {} %)  ".format(A.HardAttack,B.HardAttack,100*(divide(B.HardAttack,A.HardAttack)-1))
    txt += "\nSMA  |   {}    |   {}  (+ {} %)  ".format(A.SoftMeleeAttack,B.SoftMeleeAttack,100*(divide(B.SoftMeleeAttack,
                                                                                                 A.SoftMeleeAttack)-1))
    txt += "\nHMA  |   {}    |   {}  (+ {} %)  ".format(A.HardMeleeAttack,B.HardMeleeAttack,100*(divide(B.HardMeleeAttack,
                                                                                                 A.HardMeleeAttack)-1))
    txt += "\nDEF  |   {}    |   {}  (+ {} %)  ".format(A.Defense,B.Defense,100*(divide(B.Defense,A.Defense)-1))

    txt += "\nBRK  |   {}    |   {}  (+ {} %)  ".format(A.Breakthrought,B.Breakthrought,100*(divide(B.Breakthrought,
                                                                                                    A.Breakthrought)-1))
    txt += "\nARM  |   {}    |   {}  (+ {} %)  ".format(A.Armor,B.Armor,100*(divide(B.Armor,A.Armor)-1))
    txt += "\nPRC  |   {}    |   {}  (+ {} %)  ".format(A.Piercing,B.Piercing,100*(divide(B.Piercing,A.Piercing)-1))
    txt += "\nHRD  |   {}    |   {}  (+ {} %)  ".format(A.Hardness,B.Hardness,100*(divide(B.Hardness,A.Hardness)-1))

    txt +="\n \n"
    print(txt)
    



######## TESTING LINES
Compare_Company("Guardsmens_100A","Guardsmens_100B")
Compare_Company("Guardsmens_100B","Spaces_100A")