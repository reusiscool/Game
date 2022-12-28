from math import dist

import pygame

from baseEnemy import BaseEnemy, EnemyStats
from baseProjectile import BaseProjectile
from manaLoot import ManaLoot
from move import Move


class ShootingEnemy(BaseEnemy):
    def __init__(self, image_list: list[pygame.Surface], es: EnemyStats):
        super().__init__(image_list, es)

    def attack(self, board):
        self.cur_attack_time += 1
        if self.cur_attack_time >= self.attack_time:
            vecx, vecy = board.player.x - self.x, board.player.y - self.y
            dist_to_player = dist(self.pos, board.player.pos)
            if dist_to_player <= self.attack_distance:
                bsurf = pygame.Surface((10, 10))
                bsurf.fill('red')
                vec = Move(vecx, vecy, normalize=True)
                vec.amplify(10)
                b = BaseProjectile(self.pos, 10, [bsurf], 420, self, vec.vector, 20)
                board.add_projectile(b)
            self.cur_attack_time = 0

    def update(self, board):
        super().update(board)
        if self.health <= 0:
            board.add_projectile(ManaLoot(self.pos, 20))
            return
