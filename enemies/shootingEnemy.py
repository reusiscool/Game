from math import dist

from enemies.baseEnemy import BaseEnemy, EnemyStats
from mixer import Mixer
from utils.savingConst import SavingConstants
from utils.utils import load_image
from weapons.baseProjectile import BaseProjectile
from utils.move import Move


class ShootingEnemy(BaseEnemy):
    def attack(self, board):
        self.cur_attack_time += 1
        if self.cur_attack_time >= self.stats.attack_time:
            vecx, vecy = board.player.x - self.x, board.player.y - self.y
            dist_to_player = dist(self.pos, board.player.pos)
            if dist_to_player <= self.stats.attack_distance:
                Mixer().on_ability()
                image_list = [load_image('enemy_ability',
                                         f'enemy_ability{i}.png',
                                         color_key='white')
                              for i in range(6)]
                vec = Move(vecx, vecy, normalize=True)
                vec.amplify(10)
                b = BaseProjectile(self.pos, 10, image_list + image_list[::-1],
                                   420, self, vec.vector, self.stats.damage)
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
