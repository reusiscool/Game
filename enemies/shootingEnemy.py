from math import dist
import pygame

from enemies.baseEnemy import BaseEnemy, EnemyStats
from utils.savingConst import SavingConstants
from utils.utils import load_image
from weapons.baseProjectile import BaseProjectile
from utils.move import Move


class ShootingEnemy(BaseEnemy):
    def __init__(self, es: EnemyStats):
        image_list = [load_image('grass.jpg')]
        super().__init__(image_list, es)

    def attack(self, board):
        self.cur_attack_time += 1
        if self.cur_attack_time >= self.stats.attack_time:
            vecx, vecy = board.player.x - self.x, board.player.y - self.y
            dist_to_player = dist(self.pos, board.player.pos)
            if dist_to_player <= self.stats.attack_distance:
                bsurf = pygame.Surface((10, 10))
                bsurf.fill('red')
                vec = Move(vecx, vecy, normalize=True)
                vec.amplify(10)
                b = BaseProjectile(self.pos, 10, [bsurf], 420, self, vec.vector, self.stats.damage)
                board.add_projectile(b)
            self.cur_attack_time = 0

    @property
    def token_priority(self):
        return 1

    @property
    def drop_amount(self):
        return 2

    @classmethod
    def read(cls, line, level):
        pos = eval(line[1])
        cur_hp = int(line[2])
        speed, *stats = SavingConstants().get_stats(ShootingEnemy, level)
        es = EnemyStats((*pos, 10),
                        speed, cur_hp, *stats)
        return ShootingEnemy(es)
