from random import randint

from enemies.baseEnemy import BaseEnemy
from entity import Entity
from utils.move import Move
from utils.utils import collides, vector_len, is_left, rotate
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
    def __init__(self, max_attacks=3):
        self.max_attacks = max_attacks
        self.tokens_taken = 0
        self.calls_q = []

    def update(self, board):
        self.calls_q.clear()
        self._update_visibility(board)
        self._update_behaviour(board)

    def _update_visibility(self, board):
        for enemy1 in board.get_enemies(board.player.pos, board.update_distance):
            enemy1: BaseEnemy
            if has_clear_sight(board, enemy1) and\
                    dist(board.player.pos, enemy1.pos) <= enemy1.stats.detect_range:
                self.calls_q.append(enemy1.pos)

    def _update_behaviour(self, board):
        from surroundings.board import Board

        board: Board
        px, py = board.player.pos
        enemy_list = board.get_enemies(board.player.pos, board.update_distance)
        enemy_list.sort(key=lambda x: x.token_priority)
        owed = 0
        for enemy1 in enemy_list:
            enemy1: BaseEnemy
            vecx = px - enemy1.x
            vecy = py - enemy1.y
            dist_to_player = dist((px, py), enemy1.pos)
            if enemy1.cur_attack_time:
                enemy1.attack(board)
                owed += enemy1.attack_cost
                continue
            if dist_to_player <= enemy1.stats.min_distance:
                enemy1.move_move(Move(-vecx, -vecy, own_speed=True))
                continue
            if dist_to_player <= enemy1.stats.attack_distance:
                if self.tokens_taken < self.max_attacks:
                    enemy1.cur_attack_time += 1
                    self.tokens_taken += enemy1.attack_cost
                    continue
                self._circle_around(board, enemy1)
                continue
            for pos in self.calls_q:
                if dist(pos, enemy1.pos) <= enemy1.stats.detect_range:
                    enemy1.move_move(Move(vecx, vecy, own_speed=True))
                    enemy1.patrol_q.clear()
                    break
            else:
                if enemy1.patrol_q:
                    dest = enemy1.patrol_q[-1]
                    vecx1 = dest[0] - enemy1.x
                    vecy1 = dest[1] - enemy1.y
                    enemy1.move_move(Move(vecx1, vecy1, own_speed=True))
                    k = dist(dest, enemy1.pos)
                    if k <= enemy1.stats.speed:
                        enemy1.patrol_q.pop()
                else:
                    self._generate_patrol(board, enemy1)
        self.tokens_taken = owed

    def _generate_patrol(self, board, enemy1):
        from surroundings.board import Board

        board: Board
        closest_room = None
        dst = float('inf')
        for room in board.reader.level.get_rooms(enemy1.tile_pos(board.tile_size), 10):
            room_pos = room.pos_to_tiles(board.tile_size)
            k = dist(room_pos, enemy1.pos)
            if k < dst:
                closest_room = room
                dst = k
        for _ in range(5):
            x = randint(closest_room.rect.left * board.tile_size, (closest_room.rect.right - 1) * board.tile_size)
            y = randint(closest_room.rect.top * board.tile_size, (closest_room.rect.bottom - 1) * board.tile_size)
            enemy1.patrol_q.append((x, y))
        if not closest_room.rect.collidepoint(enemy1.tile_pos(board.tile_size)):
            enemy1.patrol_q.append(closest_room.pos_to_tiles(board.tile_size))

    def _circle_around(self, board, enemy1):
        px, py = board.player.pos
        vecx = px - enemy1.x
        vecy = py - enemy1.y
        close_enemies = board.get_enemies(enemy1.pos, 50)
        close_enemies.remove(enemy1)
        for i in range(len(close_enemies) - 1, -1, -1):
            if dist(close_enemies[i].pos, enemy1.pos) > 20:
                close_enemies.pop(i)
        if not close_enemies:
            if enemy1.going_left:
                vec = rotate((vecx, vecy), 90)[1]
            else:
                vec = rotate((vecx, vecy), 90)[0]
        else:
            closest_enemy = None
            dst = 101
            for e in close_enemies:
                k = dist(enemy1.pos, e.pos)
                if k < dst:
                    closest_enemy = e
                    dst = k
            vec = rotate((vecx, vecy), 90)
            if is_left(enemy1.pos, board.player.pos, closest_enemy.pos):
                vec = vec[0]
                enemy1.going_left = False
            else:
                vec = vec[1]
                enemy1.going_left = True
        enemy1.move_move(Move(vec[0], vec[1], own_speed=True))
