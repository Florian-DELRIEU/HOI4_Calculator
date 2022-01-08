
def set_LeaderSkills(Regiment):
    Regiment.__SoftAttack *= 1.1**Regiment.Leader.Attack_skill
    Regiment.__HardAttack *= 1.1**Regiment.Leader.Attack_skill
    Regiment.__SoftMeleeAttack *= 1.1**Regiment.Leader.Attack_skill
    Regiment.__HardMeleeAttack *= 1.1**Regiment.Leader.Attack_skill
    Regiment.__Defense *= 1.1**Regiment.Leader.Defense_skill
    Regiment.__Breakthrought *= 1.1**Regiment.Leader.Defense_skill