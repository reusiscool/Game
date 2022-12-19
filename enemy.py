from math import dist

from entity import Entity
from states import Stat
from manaLoot import ManaLoot


class Enemy(Entity):
    def __init__(self, pos, hitbox_size, image_list, speed=2, health=0, max_health=0):
        super().__init__(pos, hitbox_size, image_list, speed, health, max_health)
        self.player_pos = None
        self.dist = 30

    def update(self, board):
        super().update(board)
        if self.stats[Stat.Health] <= 0:
            board.add_projectile(ManaLoot(self.pos, 20))
            return
        if self.player_pos and dist(board.player.pos, self.pos) <= self.dist:
            return
        if board.has_clear_sight(self):
            self.player_pos = board.player.pos
        if self.player_pos:
            if dist(self.player_pos, self.pos) <= self.stats[Stat.Speed]:
                self.player_pos = None
            else:
                self.move_coords(self.player_pos[0] - self.x, self.player_pos[1] - self.y, own_speed=True)
