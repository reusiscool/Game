from math import dist

from enemies.baseEnemy import BaseEnemy, EnemyStats
from loot.healItemLoot import HealItemLoot
from loot.healthLoot import HealthLoot
from loot.manaLoot import ManaLoot
from utils.move import Move


class Enemy(BaseEnemy):
    """Better replace. Outdated"""
    def __init__(self, image_list, es: EnemyStats):
        super().__init__(image_list, es)
        self.loot_table = (ManaLoot, HealthLoot, HealItemLoot)

    @property
    def attack_cost(self):
        return 2

    def attack(self, board):
        self.cur_attack_time += 1
        if self.cur_attack_time >= self.stats.attack_time:
            vecx, vecy = board.player.x - self.x, board.player.y - self.y
            dist_to_player = dist(self.pos, board.player.pos)
            if dist_to_player <= self.stats.attack_distance:
                board.player.damage(self.stats.damage)

                board.player.move_move(Move(vecx, vecy, 10, own_speed=True))
                board.player.move_move(Move(vecx, vecy, 7, own_speed=True))
                board.player.move_move(Move(vecx, vecy, 5, own_speed=True))
            self.cur_attack_time = 0
            self.move_move(Move(-vecx, -vecy, 7, own_speed=True))
