
def apply_Terrain(Battle):
    ATK = Battle.ATK["Regiment"]
    DEF = Battle.DEF["Regiment"]
    Terrain = Battle.Terrain

    ATK.SoftAttack    *= Terrain.Attack_malus
    ATK.HardAttack    *= Terrain.Attack_malus
    ATK.Breakthrought *= Terrain.Defense_malus
