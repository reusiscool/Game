from enemies.baseEnemy import BaseEnemy, EnemyStats
from player import Player
from utils.move import Move
from utils.savingConst import SavingConstants


class DashEnemy(BaseEnemy):
    def __init__(self, es: EnemyStats):
        super().__init__(es)
        self.leap_time = 15
        self.token_time = 0

    @property
    def drop_amount(self):
        return 2

    @property
    def token_priority(self):
        return self.token_time

    @property
    def attack_cost(self):
        return 2

    def update(self, board):
        super().update(board)
        self.token_time = max(0, self.token_time - 1)

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
            self.token_time = self.leap_time + self.stats.attack_time * 3
        elif self.cur_attack_time >= self.stats.attack_time * 2 + self.leap_time:
            self.cur_attack_time = 0

    @classmethod
    def read(cls, line, level):
        pos = eval(line[1])
        cur_hp = int(line[2])
        speed, *stats = SavingConstants().get_stats(DashEnemy, level)
        es = EnemyStats((*pos, 10),
                        speed, cur_hp, *stats)
        return DashEnemy(es)
