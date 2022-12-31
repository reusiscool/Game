from baseEnemy import BaseEnemy
from entity import Entity
from move import Move
from utils import collides, vector_len
from math import dist


def has_clear_sight(board, entity1: Entity, entity2: Entity = None) -> bool:
    if entity2 is None:
        entity2 = board.player

    cx, cy = (entity1.x + entity2.x) / 2, (entity1.y + entity2.y) / 2
    d = vector_len((entity1.x - entity2.x, entity1.y - entity2.y)) / 2
    p1, p2 = entity1.pos, entity2.pos
    p1 = tuple(int(i) for i in p1)
    p2 = tuple(int(i) for i in p2)

    for obj in board.get_objects((cx, cy), d):
        if obj in (entity1, entity2):
            continue
        if collides(p1, p2, *map(int, (*obj.rect.topleft, *obj.rect.size))):
            return False
    return True


class EnemyAI:
    def __init__(self):
        self.calls_q = []

    def update(self, board):
        self.calls_q.clear()
        self._update_visibility(board)
        self._update_behaviour(board)

    def _update_visibility(self, board):
        for enemy1 in board.get_enemies(board.player.pos, board.update_distance):
            enemy1: BaseEnemy
            if has_clear_sight(board, enemy1) and dist(board.player.pos, enemy1.pos) <= enemy1.stats.detect_range:
                self.calls_q.append(enemy1.pos)

    def _update_behaviour(self, board):
        px, py = board.player.pos
        for enemy1 in board.get_enemies(board.player.pos, board.update_distance):
            enemy1: BaseEnemy
            vecx = px - enemy1.x
            vecy = py - enemy1.y
            dist_to_player = dist((px, py), enemy1.pos)
            if enemy1.cur_attack_time:
                enemy1.attack(board)
            if dist_to_player <= enemy1.stats.min_distance:
                enemy1.move_move(Move(-vecx, -vecy, own_speed=True))
                continue
            if dist_to_player <= enemy1.stats.attack_distance:
                enemy1.cur_attack_time += 1
                continue
            for pos in self.calls_q:
                if dist(pos, enemy1.pos) <= enemy1.stats.detect_range:
                    enemy1.move_move(Move(vecx, vecy, own_speed=True))
                    break
