from enemies.baseEnemy import BaseEnemy, EnemyStats
from loot.healItemLoot import HealItemLoot
from loot.healthLoot import HealthLoot
from loot.manaLoot import ManaLoot
from player import Player
from utils.move import Move
from utils.utils import load_image


class DashEnemy(BaseEnemy):
    def __init__(self, es: EnemyStats):
        image_list = [load_image('grass.jpg')]
        super().__init__(image_list, es)
        self.loot_table = (ManaLoot, HealthLoot, HealItemLoot)
        self.leap_time = 15

    @property
    def attack_cost(self):
        return 2

    def _move_x(self, dx, map_):
        if not dx:
            return
        self.x += dx
        rect = self.rect
        for obj in map_:
            r = obj.rect
            if rect.colliderect(r):
                self.collided = True
                if self.cur_attack_time >= self.stats.attack_time and isinstance(obj, Player):
                    self.cur_attack_time = 0
                    obj.damage(20)
                if dx > 0:
                    rect.right = r.left
                else:
                    rect.left = r.right
                self.x = rect.x

    def _move_y(self, dy, map_):
        if not dy:
            return
        self.y += dy
        rect = self.rect
        for obj in map_:
            r = obj.rect
            if rect.colliderect(r):
                self.collided = True
                if self.cur_attack_time >= self.stats.attack_time and isinstance(obj, Player):
                    self.cur_attack_time = 0
                    obj.damage(20)
                if dy > 0:
                    rect.bottom = r.top
                else:
                    rect.top = r.bottom
                self.y = rect.y

    def attack(self, board):
        self.cur_attack_time += 1
        if self.cur_attack_time == self.stats.attack_time:
            vecx, vecy = board.player.x - self.x, board.player.y - self.y
            mv = Move(vecx, vecy, duration=self.leap_time, own_speed=True)
            mv.amplify(3)
            self.move_move(mv)
        elif self.cur_attack_time >= self.stats.attack_time * 2 + self.leap_time:
            self.cur_attack_time = 0
