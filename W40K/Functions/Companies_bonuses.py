import numpy as np

def setCompanies_DEFBRK_bonus(object):
    # sourcery skip: merge-duplicate-blocks, remove-pass-elif, remove-redundant-if, switch
    assert object.Class == "Company" , "Must be an Company object"

    if object.Unit.Class == "Infantry":
        object.Defense *= 20
        object.Breaktrought *= 2

    elif object.Unit.Class == "Tank":

    # Tank types
        if object.Unit.Type == "Chariot":  # Like armored car
            object.Defense *= 2
            object.Breaktrought *= 10
        elif object.Unit.Type == ("Tank" or ""):  # Medium tank
            object.Defense *= 5
            object.Breaktrought *= 30
        elif object.Unit.Type == "Heavy":
            object.Defense *= 6
            object.Breaktrought *= 40
        elif object.Unit.Type == "SuperHeavy":
            object.Defense *= 10
            object.Breaktrought *= 70

    # SP artillery types
        if object.Unit.Type == "Chariot SP Artillery":  # Light
            object.Defense *= 2
            object.Breaktrought *= 10
        elif object.Unit.Type == ("Tank SP Artillery" or "SP Artillery"):  # Medium tank
            object.Defense *= 5
            object.Breaktrought *= 30
        elif object.Unit.Type == "Heavy SP Artillery":
            object.Defense *= 6
            object.Breaktrought *= 40
        elif object.Unit.Type == "SuperHeavy SP Artillery":
            object.Defense *= 10
            object.Breaktrought *= 70

    # Destroyer types
        if object.Unit.Type == "Chariot Destroyer":  # Light
            object.Defense      *= 4
            object.Breaktrought *= 2
        elif object.Unit.Type == ("Tank Destroyer" or "Destroyer"):  # Medium tank
            object.Defense      *= 5
            object.Breaktrought *= 3
        elif object.Unit.Type == "Heavy Destroyer":
            object.Defense      *= 4
            object.Breaktrought *= 2
        elif object.Unit.Type == "SuperHeavy Destroyer":
            object.Defense      *= 7
            object.Breaktrought *= 4

    elif object.Unit.Class == "Walker":
        pass

    else:
        return AttributeError , "Company class not found, must be Infantry, Tank or Walker"