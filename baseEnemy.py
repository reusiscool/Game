from abc import ABC, abstractmethod
from dataclasses import dataclass
import pygame

from entity import Entity, EntityStats, Team


@dataclass(frozen=True, slots=True)
class EnemyStats:
    """
    :param EntityStats: (square, speed, health, max_health)
    :param int: detect_range
    :param int: attack_distance
    :param int: attack_time
    :param int: damage
    :param int: min_distance
    """
    ents: EntityStats
    detect_range: int
    attack_distance: int
    attack_time: int
    damage: int
    min_distance: int = 0


class BaseEnemy(Entity, ABC):
    def __init__(self, image_list: list[pygame.Surface], es: EnemyStats):
        super().__init__(image_list, es.ents)
        self.detect_range = es.detect_range
        self.player_pos = None
        self.attack_distance = es.attack_distance
        self.attack_time = es.attack_time
        self.cur_attack_time = 0
        self.attack_damage = es.damage
        self.min_distance = es.min_distance
        self.team = Team.Enemy

    def update(self, board):
        board.pop_enemy(self)
        self.collided = False
        dx, dy = self.calc_movement()
        ls = board.get_objects(self.pos, 100)
        self._move_x(dx, ls)
        self._move_y(dy, ls)
        if self.health > 0:
            board.add_enemy(self)

    @abstractmethod
    def attack(self, *args, **kwargs):
        pass
