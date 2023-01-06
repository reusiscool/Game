from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import choice
import pygame

from utils.customFont import single_font
from entity import Entity, EntityStats, Team


@dataclass(slots=True)
class EnemyStats(EntityStats):
    detect_range: int
    attack_distance: int
    attack_time: int
    damage: int
    min_distance: int = 0


class BaseEnemy(Entity, ABC):
    def __init__(self, image_list: list[pygame.Surface], es: EnemyStats):
        super().__init__(image_list, es)
        self.stats = es
        self.player_pos = None
        self.cur_attack_time = 0
        self.font = single_font('large_font')
        self.loot_table = []

    def update(self, board):
        board.pop_enemy(self)
        self.collided = False
        dx, dy = self.calc_movement()
        ls = board.get_objects(self.pos, 100)
        self._move_x(dx, ls)
        self._move_y(dy, ls)
        if self.stats.health > 0:
            board.add_enemy(self)
        elif self.loot_table:
            board.add_noncollider(choice(self.loot_table)(self.pos, 20))

    @property
    def team(self):
        return Team.Enemy

    @abstractmethod
    def attack(self, *args, **kwargs):
        pass
