from math import dist

from entity import Entity
from utils import draw_line


class Enemy(Entity):
    def __init__(self, pos, hitbox_size, image, speed=2, health=0, max_health=0):
        super().__init__(pos, hitbox_size, image, speed, health, max_health)
        self.player_pos = None
        self.dist = 30

    def has_clear_sight(self, player: Entity, box_board: dict[dict[int]], tile_size) -> bool:
        sx, sy = self.pos
        sx //= tile_size
        sy //= tile_size

        px, py = player.pos
        px //= tile_size
        py //= tile_size

        for x, y in draw_line(sx, sy, px, py):
            if y not in box_board:
                continue
            if x not in box_board[y]:
                continue
            return False
        return True

    def update(self, board):
        super().update(board)
        if self.has_clear_sight(board.player, board.boxes, board.tile_size):
            self.player_pos = board.player.pos
        if self.player_pos:
            if dist(self.player_pos, self.pos) <= self.dist:
                self.player_pos = None
            else:
                self.move_coords(self.player_pos[0] - self.x, self.player_pos[1] - self.y, own_speed=True)
