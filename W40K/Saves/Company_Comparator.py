from MyPack.Convert import *

Companies_Data = Csv2Dict("SaveCompanies.csv")
Compare_list = ["Guardsmens_100A","LOL_company"]

for cur in Compare_list:
    if cur not in Companies_Data.keys():            # Si company n'existe pas dans save
        del Compare_list[Compare_list.index(cur)]   # La supprimer de la comparaison

