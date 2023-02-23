from dataclasses import dataclass
from random import randint

from entity import Entity, EntityStats, Team
from skill import Skill
from utils.move import Move
from utils.utils import normalize, load_image
from surroundings.rooms import RoomType
from effects import Effect, EffectContainer


@dataclass(slots=True)
class PlayerStats(EntityStats):
    mana: int
    max_mana: int
    dash_cooldown: int
    dash_speed: int
    gold: int
    skill_points: int

    def add_mana(self, amount):
        self.mana = min(self.max_mana, self.mana + amount)


class Player(Entity):
    def __init__(self, ps: PlayerStats, inventory, weapons, ability):
        ls = []
        for i in range(17):
            for _ in range(7):
                ls.append(load_image('player', f'player{i}.png', color_key='white'))
        super().__init__(ls, ps)
        self.inventory = inventory
        self.stats = ps
        self.dash_current_cooldown = 0
        self.weapon_list = weapons
        self.ability = ability
        self.try_attack = False
        self.try_sec_attack = False
        self.weapon_index = False
        self.looking_direction = (1, 1)
        self.is_interacting = False
        self.is_passing = False
        self.highlighted = False
        self.is_blocking = False
        self.skills: list[tuple[Skill, int]] = []

    @property
    def reveal_distance(self):
        for sk, lvl in self.skills:
            if sk == Skill.MiscMapDist:
                return 4 + lvl
        return 4

    @property
    def revealed_rooms(self) -> list[RoomType]:
        ls = []
        for sk, lvl in self.skills:
            if sk == Skill.MiscMapKeyPortal:
                ls.append(RoomType.Key)
                ls.append(RoomType.Portal)
        return ls

    @property
    def team(self):
        return Team.Player

    @property
    def _has_block(self):
        return not not [i for i in self.skills if i[0] == Skill.BerBlock]

    @property
    def _receive_damage_multiplier(self):
        if self._has_block and self.is_blocking:
            return 0.5
        return 1

    @property
    def _movement_multiplier(self):
        k = super()._movement_multiplier
        if self._has_block and self.is_blocking:
            return k * 0.5
        return k

    @property
    def _crit_chance(self):
        """measured in per cents"""
        if not [i for i in self.skills if i[0] == Skill.BerCrit]:
            return 0
        return 20

    @property
    def has_crited(self):
        return randint(1, 100) <= self._crit_chance

    def render(self, surf, camera_x, camera_y):
        self.weapon_list[self.weapon_index].render(surf, camera_x, camera_y, self)
        super().render(surf, camera_x, camera_y)

    def change_weapon(self):
        self.weapon_index = not self.weapon_index

    def secondary_attack(self):
        self.try_sec_attack = True

    def attack(self):
        self.try_attack = True

    def update(self, board):
        super().update(board)
        self.dash_current_cooldown = max(0, self.dash_current_cooldown - 1)
        self.weapon_list[0].update()
        self.weapon_list[1].update()
        self.ability.update()
        if self.try_attack:
            self.weapon_list[self.weapon_index].attack(board, self)
            self.try_attack = False
        if self.try_sec_attack:
            self.ability.attack(board, self)
            self.try_sec_attack = False

    def move_input(self, x, y):
        mv = Move(x, y, own_speed=True, normalize=True)
        self.move_move(mv)

    def dash(self, dx, dy):
        dx, dy = normalize(dx, dy)
        if self.dash_current_cooldown:
            return
        self.effects.append(EffectContainer(Effect.Slowness, 4, 30))
        self.effects.append(EffectContainer(Effect.Slowness, 4, 30))
        self.effects.append(EffectContainer(Effect.Slowness, 4, 20))
        self.dash_current_cooldown = self.stats.dash_cooldown
        self.move_q.append(Move(dx * self.stats.dash_speed, dy * self.stats.dash_speed, 10))
        self.move_q.append(Move(dx * self.stats.dash_speed, dy * self.stats.dash_speed, 7))
        self.move_q.append(Move(dx * self.stats.dash_speed, dy * self.stats.dash_speed, 4))
        self.move_q.append(Move(dx * self.stats.dash_speed, dy * self.stats.dash_speed, 2))

    def add_health(self, amount):
        self.stats.heal(amount)

    def add_mana(self, amount):
        self.stats.add_mana(amount)

    def serialize(self):
        return [[self.inventory.size]] + [self._serialize_stats()]\
               + self._serialize_tools() + self._serialize_inventory()

    def _serialize_stats(self):
        return tuple(int(i) for i in self.pos), self.stats.speed, self.stats.health,\
               self.stats.max_health, self.stats.mana, self.stats.max_mana,\
               self.stats.dash_cooldown, self.stats.dash_speed, self.stats.gold, self.stats.skill_points

    def _serialize_tools(self):
        ls = []
        for weapon in self.weapon_list:
            ls.append(weapon.serialize())
        ls.append(self.ability.serialize())
        return ls

    def _serialize_inventory(self):
        ls = []
        for item in self.inventory.items:
            ls.append(item.serialize())
        return ls
