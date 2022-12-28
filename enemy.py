from baseEnemy import BaseEnemy, EnemyStats
from manaLoot import ManaLoot
from move import Move


class Enemy(BaseEnemy):
    def __init__(self, image_list, es: EnemyStats):
        super().__init__(image_list, es)

    def attack(self, player, dist_to_player):
        vecx, vecy = player.x - self.x, player.y - self.y
        self.cur_attack_time += 1
        if self.cur_attack_time >= self.attack_time:
            if dist_to_player <= self.attack_distance:
                player.damage(self.attack_damage)

                player.move_move(Move(vecx, vecy, 10, own_speed=True))
                player.move_move(Move(vecx, vecy, 7, own_speed=True))
                player.move_move(Move(vecx, vecy, 5, own_speed=True))
            self.cur_attack_time = 0
            self.move_move(Move(-vecx, -vecy, 7, own_speed=True))

    def update(self, board):
        super().update(board)
        if self.health <= 0:
            board.add_projectile(ManaLoot(self.pos, 20))
            return
        # if self.cur_attack_time:
        #     self.attack(board)
        #     return
        # vecx, vecy = board.player.x - self.x, board.player.y - self.y
        # dist_to_player = vector_len((vecx, vecy))
        # if self.player_pos and dist_to_player <= self.attack_distance:
        #     self.cur_attack_time = 1
        #     return
        # if board.has_clear_sight(self) and dist_to_player < self.detect_range:
        #     self.player_pos = board.player.pos
        #     if vecx > vecy:
        #         self.looking_direction = (1, 0)
        #     else:
        #         self.looking_direction = (0, 1)
        # if self.player_pos:
        #     if dist(self.player_pos, self.pos) <= self.speed:
        #         self.player_pos = None
        #     else:
        #         self.move_move(Move(self.player_pos[0] - self.x,
        #                             self.player_pos[1] - self.y,
        #                             own_speed=True, normalize=True))
