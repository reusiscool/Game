from enum import Enum


class Skill(Enum):
    BerBlock = 1
    BerCrit = 2
    BerVamp = 3

    MiscMapDist = 10
    MiscMapKeyPortal = 11
    MiscInventorySlot = 12

    TankHealth = 20

    def get_desc(self):
        if self not in skill_desc:
            raise NotImplementedError
        return skill_desc[self]

    def get_stats(self):
        if self not in skill_stats:
            raise ValueError
        return skill_stats[self]

    def get_price(self, level):
        pass


# todo prices
skill_price = {}
skill_stats = {
    Skill.BerBlock: 0,
    Skill.BerVamp: 0,
    Skill.TankHealth: (10, 0.1)
}
skill_desc = {
    Skill.BerBlock: ('Block', 'Hold mouse button to block damage slowing down'),
    Skill.BerCrit: ('Crit', 'Unlocks ability to do additional damage by chance'),
    Skill.BerVamp: ('Vampire', 'Can heal by attacking enemies'),
    Skill.MiscMapDist: ('Map reveal distance', 'Increases map reveal distance'),
    Skill.MiscMapKeyPortal: ('Map aura reveal', 'Map reveals key and portal rooms'),
    Skill.MiscInventorySlot: ('Inventory slot', 'Adds one additional inventory slot'),
    Skill.TankHealth: ('Health buffer', 'Increases max health as well as decreases player speed')
}
