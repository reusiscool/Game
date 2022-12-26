from abc import ABC, abstractmethod
from dataclasses import dataclass
import pygame

from entity import Entity, EntityStats


@dataclass(frozen=True, slots=True)
class EnemyStats:
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

    @abstractmethod
    def attack(self, *args, **kwargs):
        pass
