from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from enemies.lootTable import EnemyLootTable
from loot.moneyLoot import MoneyLoot
from mixer import Mixer
from entity import Entity, EntityStats, Team
from utils.savingConst import SavingConstants
from utils.utils import load_image


@dataclass(slots=True)
class EnemyStats(EntityStats):
    detect_range: int
    attack_distance: int
    attack_time: int
    damage: int
    min_distance: int = 0


class BaseEnemy(Entity, ABC):
    def __init__(self, es: EnemyStats):
        image_list = [load_image('enemies', 'enemy.png', color_key='white')]
        super().__init__(image_list, es)
        self.stats = es
        self.player_pos = None
        self.cur_attack_time = 0
        self.loot_table = EnemyLootTable()
        self.going_left = False
        self.patrol_q = []

    @property
    def attack_cost(self):
        return 1

    def update(self, board):
        board.pop_enemy(self)
        self.collided = False
        dx, dy = self.calc_movement()
        ls = board.get_objects(self.pos, 100)
        self._move_x(dx / 3 if self.patrol_q else dx, ls)
        self._move_y(dy / 3 if self.patrol_q else dy, ls)
        if self.stats.health > 0:
            board.add_enemy(self)
            return
        Mixer.on_death()
        if self.loot_table:
            for _ in range(self.drop_amount):
                type_ = self.loot_table.roll()
                if type_ == MoneyLoot:
                    obj = type_(self.pos, SavingConstants().gold_drop[board.reader.level.level_number - 1])
                else:
                    obj = type_(self.pos)
                if obj is not None:
                    board.add_noncollider(obj)

    @property
    @abstractmethod
    def drop_amount(self):
        return ...

    @property
    def team(self):
        return Team.Enemy

    @abstractmethod
    def attack(self, *args, **kwargs):
        pass

    def serialize(self) -> Tuple[int, tuple[int, int], int]:
        return SavingConstants().get_const(type(self)),\
               (int(self.x), int(self.y)), self.stats.health

    @property
    @abstractmethod
    def token_priority(self):
        return ...
