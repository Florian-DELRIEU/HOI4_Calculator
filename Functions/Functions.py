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
