from utils.singleton import Singleton


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
    return 20 - lvl // 2


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


class SavingConstants(metaclass=Singleton):
    def __init__(self):
        from enemies.dashEnemy import DashEnemy
        from enemies.shootingEnemy import ShootingEnemy
        from surroundings.trap import Trap
        from weapons.sword import Sword
        from interactables.weaponLoot import WeaponLoot
        from interactables.portal import Portal
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
        from loot.skillPointLoot import SkillPointLoot
        from puzzles.ticPuzzle import TicTacToePuzzle
        from puzzles.liarPuzzle import LiarPuzzle
        from puzzles.silverPuzzle import SilverPuzzle
        from weapons.dropSwords import GoldenSword
        from weapons.dropSwords import ManaSword

        self._types = [DashEnemy, ShootingEnemy, KeyItemLoot, Trap, WeaponLoot, TicTacToePuzzle, LiarPuzzle, Portal,
                       HealItem, KeyItem, HealItemLoot, HealthLoot, ManaLoot, ManaItem, ManaItemLoot, Shop, AbilityLoot,
                       Sword, Ability, MoneyLoot, DarkShop, GoldenSword, ManaSword, SkillPointLoot, SilverPuzzle]
        self._const = dict()
        for i, var in enumerate(self._types):
            self._const[var] = i

        # 4 rarities, 10 levels
        self.avg_weapon_score = (50, 62, 75, 90)
        self.enemies_per_room = (2, 3, 3, 3, 4, 4, 4, 5, 5, 5)
        self.level_size = (40, 40, 40, 60, 60, 60, 80, 80, 80, 100)
        self.gold_drop = (8, 9, 10, 11, 12, 13, 14, 16, 18, 20)
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
             (HealthLoot, lambda x: (15, health_cost(x))),
             (ManaLoot, lambda x: (25, mana_cost(x)))],

            [(ManaItemLoot, lambda x: (35, healitem_cost(x))),
             (HealItemLoot, lambda x: (20, healitem_cost(x))),
             (WeaponLoot, lambda x: (Sword.generate(2, x + 2), 80 + x * 25))],

            [(AbilityLoot, lambda x: (Ability.generate(2, x + 2), 80 + x * 25)),
             (WeaponLoot, lambda x: (Sword.generate(3, x + 3), 100 + x * 40))]
        ]
        self.dark_shop_items = [
            [
                (ManaItemLoot, lambda x: (35, healitem_cost(x))),
                (HealItemLoot, lambda x: (20, healitem_cost(x)))
            ],

            [
                (ManaItemLoot, lambda x: (45, healitem_cost(x))),
                (HealItemLoot, lambda x: (30, healitem_cost(x)))
            ],

            [
                (SkillPointLoot, lambda x: (x * 10 + 20,))
            ],

            [
                (AbilityLoot, lambda x: (Ability.generate(3, x + 3), 100 + x * 40))
            ]
        ]
        self.rarity_color = ['Grey', 'Green', 'Purple', 'Yellow']
        self.rarity_names = ['Common', 'Uncommon', 'Epic', 'Legendary']

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

    def load(self, line):
        type_ = self.get_type(int(line[0]))
        return type_.read(line)
