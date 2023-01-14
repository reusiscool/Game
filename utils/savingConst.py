from random import randint, choice

import pygame


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
    """returns minimum and range"""
    return 6, 14 + lvl * 4


def sword_range(lvl):
    return 30, 60 + lvl * 5


def sword_angle(lvl):
    return 10, 20 + lvl * 2


def sword_cooldown(lvl):
    return 10, 35 + lvl * 3


def sword_knockback(lvl):
    return 20, 30 + lvl * 3


def health_cost(lvl):
    return 5 + lvl * 2


def mana_cost(lvl):
    return 2 + lvl * 2


def healitem_cost(lvl):
    return 10 + lvl * 2


def manaitem_cost(lvl):
    return 5 + lvl * 2


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
        from items.healItem import HealItem
        from items.keyItem import KeyItem
        from loot.healthLoot import HealthLoot
        from loot.manaLoot import ManaLoot
        from loot.healItemLoot import HealItemLoot
        from items.manaItem import ManaItem
        from loot.manaItemLoot import ManaItemLoot
        from interactables.shop import Shop
        from interactables.abilityLoot import AbilityLoot
        from loot.keyItemLoot import KeyItemLoot
        from weapons.ability import Ability
        from loot.moneyLoot import MoneyLoot
        from interactables.darkShop import DarkShop
        from loot.mapDistLoot import MapDistLoot
        from loot.mapRoomLoot import MapRoomLoot
        from surroundings.rooms import RoomType

        self._const = {
            DashEnemy: 1,
            ShootingEnemy: 2,
            keyItemLoot.KeyItemLoot: 3,
            Trap: 4,
            WeaponLoot: 5,
            BasePuzzle: 6,
            Portal: 7,
            HealItem: 8,
            KeyItem: 9,
            HealItemLoot: 10,
            HealthLoot: 11,
            ManaLoot: 12,
            ManaItem: 13,
            ManaItemLoot: 14,
            Shop: 15,
            AbilityLoot: 16,
            Sword: 17,
            Ability: 18,
            MoneyLoot: 19,
            DarkShop: 20,
            MapDistLoot: 21,
            MapRoomLoot: 22
        }
        self._types = {}
        for i in self._const:
            self._types[self._const[i]] = i

        # self.level = None

        # 4 rarities, 10 levels
        self.avg_weapon_score = (50, 62, 75, 90)
        self.enemies_per_room = (2, 3, 3, 3, 4, 4, 4, 5, 5, 5)
        self.level_size = (40, 40, 40, 60, 60, 60, 80, 80, 80, 100)
        self.gold_drop = (3, 4, 6, 8, 10, 12, 13, 14, 15, 20)
        self.trap_chance = (7, 6, 6, 6, 5, 5, 5, 4, 4, 3)

        self._stats = {
            Trap: lambda x: (trap_damage(x), trap_cooldown(x), trap_time_up(x)),
            DashEnemy: lambda x: (dash_enemy_speed(x),
                                  dash_enemy_health(x),
                                  300, 70,
                                  dash_enemy_attack_time(x),
                                  dash_enemy_damage(x), 40),
            ShootingEnemy: lambda x: (shooting_enemy_speed(x),
                                      shooting_enemy_health(x),
                                      300, 150,
                                      shooting_enemy_attack_time(x),
                                      shooting_enemy_damage(x),
                                      100),
            Sword: lambda x: (sword_damage(x),
                              sword_range(x),
                              sword_angle(x),
                              sword_cooldown(x),
                              sword_knockback(x)),
            Ability: lambda lvl: ((45, 20 + lvl * 3),
                                  (77, 10 + lvl),
                                  (5, 5 + lvl * 3))
        }
        self.shop_items = [
            [(ManaLoot, lambda x: (20, mana_cost(x))),
             (HealthLoot, lambda x: (10, health_cost(x))),
             (HealItemLoot, lambda x: (10, healitem_cost(x))),
             (ManaItemLoot, lambda x: (20, manaitem_cost(x)))],

            [(ManaItemLoot, lambda x: (25, healitem_cost(x))),
             (HealItemLoot, lambda x: (15, healitem_cost(x))),
             (WeaponLoot, lambda lvl: (Sword.generate(2, lvl + 2), 60 + lvl * 40))],

            [(ManaItemLoot, lambda x: (35, healitem_cost(x))),
             (AbilityLoot, lambda x: (Ability.generate(2, x + 2), 60 + x * 30)),
             (WeaponLoot, lambda x: (Sword.generate(3, x + 3), 120 + x * 60))],

            [(AbilityLoot, lambda x: (Ability.generate(3, x + 3), 120 + x * 60))]
        ]
        self.dark_shop_items = [
            [(MapDistLoot, lambda x: (0,)),
             (MapRoomLoot, lambda x: (RoomType.Combat, 0))],
            [(MapDistLoot, lambda x: (40 + x * 5,))],
            [(MapDistLoot, lambda x: (40 + x * 5,))],
            [(MapDistLoot, lambda x: (40 + x * 5,))]
        ]
        self._loads = {
            WeaponLoot: lambda x: self._load_weapon_loot(x),
            KeyItemLoot: lambda x: self._load_key(x),
            Portal: lambda x: self._load_portal(x),
            HealthLoot: lambda x: self._load_mana_health(x, HealthLoot),
            ManaLoot: lambda x: self._load_mana_health(x, ManaLoot),
            ManaItemLoot: lambda x: self._load_mana_health(x, ManaItemLoot),
            HealItemLoot: lambda x: self._load_mana_health(x, HealItemLoot),
            Shop: lambda x: self._load_shop(x),
            AbilityLoot: lambda x: self._load_ability_loot(x),
            Sword: lambda x: self._load_sword(x),
            Ability: lambda x: self._load_ability(x),
            MoneyLoot: lambda x: self._load_mana_health(x, MoneyLoot),
            DarkShop: self._load_dark_shop,
            MapDistLoot: lambda line: self._load_only_pos(line, MapDistLoot),
            MapRoomLoot: self._load_map_room_loot
        }

    def get_const(self, type_) -> int:
        return self._const[type_]

    def contains(self, type_):
        return type_ in self._const

    def get_type(self, const):
        return self._types[const]

    def get_stats(self, type_, lvl):
        return self._stats[type_](lvl)

    def get_shop_items(self, rarity: int, lvl: int):
        res = []
        for ls in self.shop_items[rarity]:
            item, stats = ls
            res.append((item, stats(lvl)))
        return res

    def get_dark_shop_items(self, rarity: int, lvl: int):
        res = []
        for ls in self.dark_shop_items[rarity]:
            item, stats = ls
            res.append((item, stats(lvl)))
        return res

    def _shop_info(self, line):
        pos = eval(line[1])
        rarity = int(line[2])
        k = 3
        goods = []
        for _ in range(3):
            ls = []
            while True:
                if k == len(line) or line[k] == '/n':
                    k += 1
                    break
                ls.append(line[k])
                k += 1
            if len(ls) <= 1:
                goods.append(None)
                continue
            *line1, cost = ls
            cost = int(cost)
            item = self.load(line1)
            goods.append((item, cost))
        return pos, rarity, goods

    def _load_shop(self, line):
        from interactables.shop import Shop
        pos, rarity, goods = self._shop_info(line)
        shop = Shop(pos, rarity, goods=goods)
        return shop

    def _load_dark_shop(self, line):
        from interactables.darkShop import DarkShop
        locks = list(eval(line.pop(3)))
        pos, rarity, goods = self._shop_info(line)
        return DarkShop(pos, rarity, locks, goods=goods)

    def _load_key(self, line):
        from loot.keyItemLoot import KeyItemLoot
        pos = eval(line[1])
        id_ = int(line[2])
        return KeyItemLoot(pos, id_)

    def _load_weapon_loot(self, line):
        from interactables.weaponLoot import WeaponLoot
        pos = eval(line[1])
        return WeaponLoot(pos, self.load(line[2:]))

    def _load_sword(self, line):
        from weapons.sword import SwordStats
        from weapons.sword import Sword
        dmg = int(line[1])
        rng = int(line[2])
        angle = int(line[3])
        cd = int(line[4])
        knock = int(line[5])
        sws = SwordStats(dmg, rng, angle, cd, knock)
        return Sword(sws)

    def _load_ability_loot(self, line):
        from interactables.abilityLoot import AbilityLoot
        pos = eval(line[1])
        return AbilityLoot(pos, self.load(line[2:]))

    def _load_only_pos(self, line, type_):
        pos = eval(line[1])
        return type_(pos)

    def _load_ability(self, line):
        from weapons.baseAbility import AbilityStats
        from weapons.ability import Ability
        cd = int(line[1])
        cost = int(line[2])
        dmg = int(line[3])
        stats = AbilityStats(cd, cost, dmg)
        return Ability(stats)

    def _load_mana_health(self, line, type_):
        pos = eval(line[1])
        amount = int(line[2])
        return type_(pos, amount)

    def _load_portal(self, line):
        from interactables.portal import Portal
        locks = list(eval(line[1]))
        pos = eval(line[2])
        return Portal(pos, locks)

    def _load_map_room_loot(self, line):
        from surroundings.rooms import RoomType
        from loot.mapRoomLoot import MapRoomLoot
        pos = eval(line[1])
        room_type = RoomType(int(line[2]))
        return MapRoomLoot(pos, room_type)

    def load(self, line):
        type_ = self.get_type(int(line[0]))
        return self._loads[type_](line)
