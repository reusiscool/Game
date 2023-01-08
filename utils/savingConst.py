from random import randint


def _damage_scale(start_damage, lvl):
    return start_damage + start_damage * lvl // 12


def trap_damage(lvl):
    return _damage_scale(20, lvl)


def trap_cooldown(lvl):
    return 180 - lvl * 10


def trap_time_up(lvl):
    return 60 + lvl * 5


def shooting_enemy_speed(lvl):
    return 2.5 + lvl // 10


def dash_enemy_speed(lvl):
    return 3.5 + lvl // 10


def shooting_enemy_health(lvl):
    return 70 + lvl * 5


def dash_enemy_health(lvl):
    return 100 + lvl * 10


def shooting_enemy_attack_time(lvl):
    return 12 - lvl // 2


def dash_enemy_attack_time(lvl):
    return 30 - lvl


def shooting_enemy_damage(lvl):
    return 5 + lvl * 3 // 2


def dash_enemy_damage(lvl):
    return 20 + lvl


def sword_damage(lvl):
    return 20 + randint(0, 20) - 10 + lvl * 4


def sword_range(lvl):
    return 80 + randint(0, 60) - 30 + lvl * 5


def sword_angle(lvl):
    return 35 + randint(0, 10) - 5 + lvl * 5


def sword_cooldown(lvl):
    return 60 + randint(0, 10) - 5 - lvl * 3


def sword_knockback(lvl):
    return 60 + randint(0, 20) - 10 + lvl * 2


class SavingConstants:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SavingConstants, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        from enemies.dashEnemy import DashEnemy
        from enemies.shootingEnemy import ShootingEnemy
        from loot import keyItemLoot
        from surroundings.trap import Trap
        from weapons.sword import Sword
        from interactables.weaponLoot import WeaponLoot
        from interactables.portal import Portal
        from puzzles.basePuzzle import BasePuzzle

        self.enemies_per_room = (2, 3, 3, 3, 4, 4, 4, 5, 5, 5)
        self._const = {
            DashEnemy: 1,
            ShootingEnemy: 2,
            keyItemLoot.KeyItemLoot: 3,
            Trap: 4,
            WeaponLoot: 5,
            BasePuzzle: 6,
            Portal: 7
        }
        self._types = {}
        self.level_size = (40, 40, 40, 60, 60, 60, 80, 80, 80, 100)
        for i in self._const:
            self._types[self._const[i]] = i
        self._stats = {
            Trap: lambda x: (trap_damage(x), trap_cooldown(x), trap_time_up(x)),
            DashEnemy: lambda x: (dash_enemy_speed(x),
                                  dash_enemy_health(x),
                                  400, 70,
                                  dash_enemy_attack_time(x),
                                  dash_enemy_damage(x), 0),
            ShootingEnemy: lambda x: (shooting_enemy_speed(x),
                                      shooting_enemy_health(x),
                                      350, 150,
                                      shooting_enemy_attack_time(x),
                                      shooting_enemy_damage(x),
                                      100),
            Sword: lambda x: (sword_damage(x),
                              sword_range(x),
                              sword_angle(x),
                              sword_cooldown(x),
                              sword_knockback(x))
        }

    def get_const(self, type_) -> int:
        return self._const[type_]

    def contains(self, type_):
        return type_ in self._const

    def get_type(self, const):
        return self._types[const]

    def get_stats(self, type_, lvl):
        return self._stats[type_](lvl)
