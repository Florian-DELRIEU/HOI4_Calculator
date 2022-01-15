def round_Stats(Object):
    Dico = Object.__dict__
    for key in Dico:
        try:    Dico[key] = round(Dico[key],2)
        except: pass

def setQuantity(object, Quantity):
    """
    Modifie la quantité de :Unit: et modifie les stats en fonction
    :param Quantity: Nombre de cette unité
    """
    previous_Quantity = object.Quantity
    object.Quantity = Quantity
    quantity_factor = Quantity/previous_Quantity
# Add quantity
    try:    object.HP *= quantity_factor  # si HP est présent
    except: pass                          # sinon pass
    object.SoftAttack *= quantity_factor
    object.HardAttack *= quantity_factor
    object.SoftMeleeAttack *= quantity_factor
    object.HardMeleeAttack *= quantity_factor
    try:    object.Defense *= quantity_factor
    except: pass
    try:    object.Breakthrought *= quantity_factor
    except: pass

def check_lists(self):
    from W40K.Class.Weapons import Weapon
    for el in self.Equipement:
        assert type(el) is Weapon , "Each element of Equipement list must be a :Weapon class:"
"""
def saveInCSV(Object):
    Dico1 = Object.__dict__
    Dico2 = getFromDict(Dico1,["HP","ORG",
                               "SoftAttack","HardAttack","SoftMeleeAttack","HardMeleeAttack",
                               "Breaktrhought","Defense","Armor","Piercing","Hardness"
                               ])

    if type(Object) == Infantry: Dict2CSV(Dico2,"Saved_Infantry.csv")
    elif type(Object) == Tank: Dict2CSV(Dico2,"Saved_Tank.csv")
    elif type(Object) == Walker: Dict2CSV(Dico2,"Saved_Walker.csv")
    elif type(Object) == Weapon: Dict2CSV(Dico2,"Saved_Weapon.csv")
    elif type(Object) == Company: Dict2CSV(Dico2,"Saved_Company.csv")
    else: return TypeError , "Object must be Infantry, Walker, Tank, Weapon or Company. Save is not possible"
"""
