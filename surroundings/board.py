import csv
import os
from typing import Protocol

from enemies.enemyAI import EnemyAI
from surroundings.grassController import GrassController
from weapons.baseProjectile import BaseProjectile
from .levelReader import LevelReader
from .obs import Obs


class CollisionEntity(Protocol):
    @property
    def rect(self):
        return ...

    @property
    def pos(self) -> tuple:
        return ...

    def tile_pos(self, tile_size) -> tuple:
        return ...

    def render(self):
        pass


class UpdatableEntity(CollisionEntity, Protocol):
    def update(self, board):
        pass


class Board:
    def __init__(self, tile_size, player_, update_distance, render_distance, gen_new=False):
        self.render_distance = render_distance
        self.update_distance = update_distance
        self.player = player_
        self.tile_size = tile_size
        self.collider_map: dict[tuple, list[CollisionEntity]] = {}
        self.update_map: dict[tuple, list[UpdatableEntity]] = {}
        self.enemy_map: dict[tuple, list[UpdatableEntity]] = {}
        self.noncolliders: dict[tuple, list[CollisionEntity]] = {}
        self.floor_map: dict[tuple, list[Obs]] = {}
        self.projectiles: list[BaseProjectile] = []
        self.enemyAI = EnemyAI()
        self.reader = LevelReader(self.tile_size, gen_new)
        self.gc = GrassController(10, self.tile_size, 10)
        if gen_new:
            player_.x, player_.y = self.reader.player_room
            player_.x *= self.tile_size
            player_.y *= self.tile_size
        self.add_entity(player_)
        for gr in self.reader.grass:
            x, y = gr
            x *= self.tile_size
            y *= self.tile_size
            self.gc.add_tile((x, y))
        self.reader.load(self)
        self.dead = False

    def add_item(self, obj, map_: dict[tuple, list]):
        pos = obj.tile_pos(self.tile_size)
        if pos not in map_:
            map_[pos] = []
        map_[pos].append(obj)

    def get_items(self, pos, distance, map_: dict[tuple, list]) -> list:
        x, y = pos
        ls = []
        for ny in range(int((y - distance) // self.tile_size),
                        int((y + distance) // self.tile_size) + 1):
            for nx in range(int((x - distance) // self.tile_size),
                            int((x + distance) // self.tile_size) + 1):
                pos = (nx, ny)
                if pos not in map_:
                    continue
                map_[pos].sort(key=lambda o: sum(o.pos))
                ls += map_[pos]
        return ls

    def pop_item(self, obj, map_):
        pos = obj.tile_pos(self.tile_size)
        if pos not in map_:
            return
        map_[pos].remove(obj)

    def add_noncollider(self, obj: CollisionEntity):
        self.add_item(obj, self.noncolliders)

    def pop_loot(self, obj):
        self.pop_item(obj, self.noncolliders)

    def add_projectile(self, obj):
        self.projectiles.append(obj)

    def pop_projectile(self, obj):
        self.projectiles.remove(obj)

    def add_entity(self, obj: UpdatableEntity):
        self.add_item(obj, self.update_map)
        self.add(obj)

    def add_enemy(self, obj: UpdatableEntity):
        self.add_item(obj, self.enemy_map)
        self.add_entity(obj)

    def pop_enemy(self, obj: UpdatableEntity):
        self.pop_item(obj, self.enemy_map)
        self.pop_entity(obj)

    def add(self, obj: CollisionEntity):
        self.add_item(obj, self.collider_map)

    def pop(self, obj: CollisionEntity):
        self.pop_item(obj, self.collider_map)

    def pop_entity(self, obj: UpdatableEntity):
        self.pop(obj)
        self.pop_item(obj, self.update_map)

    def get_enemies(self, pos, distance):
        return self.get_items(pos, distance, self.enemy_map)

    def get_entities(self, pos, distance) -> list[UpdatableEntity]:
        return self.get_items(pos, distance, self.update_map)

    def get_objects(self, pos, distance) -> list[CollisionEntity]:
        return self.get_items(pos, distance, self.collider_map)

    def update(self):
        if self.dead:
            return
        self.enemyAI.update(self)
        for i in self.get_items(self.player.pos, self.update_distance, self.noncolliders):
            i.update(self)
        for i in self.projectiles:
            i.update(self)
        for i in self.get_entities(self.player.pos, self.update_distance):
            i.update(self)
        self.player.is_interacting = False
        self.player.highlighted = False
        self.gc.update()

    def render(self, surf, camera_x, camera_y, x, y):
        for floor in self.get_items((x, y), self.render_distance, self.floor_map):
            floor.render(surf, camera_x, camera_y)
        stx = int((x - self.render_distance) // self.tile_size)
        endx = int((x + self.render_distance) // self.tile_size)
        sty = int((y - self.render_distance) // self.tile_size)
        endy = int((y + self.render_distance) // self.tile_size)
        proj_map = {}
        grass_map = {}
        for i in self.projectiles:
            self.add_item(i, proj_map)
        for chunk in self.gc.retrieve_surfs((x, y), self.render_distance):
            self.add_item(chunk, grass_map)
        for ny in range(sty, endy + 1):
            for nx in range(stx, endx + 1):
                ls = []
                pos = (nx, ny)
                if pos in self.collider_map:
                    ls += self.collider_map[pos]
                if pos in proj_map:
                    ls += proj_map[pos]
                if pos in self.noncolliders:
                    ls += self.noncolliders[pos]
                if pos in grass_map:
                    ls += grass_map[pos]
                ls.sort(key=lambda o: sum(o.pos))
                for i in ls:
                    i.render(surf, camera_x, camera_y)

    def save(self):
        if self.dead:
            return
        ls = []
        for key in self.update_map:
            ls += self.update_map[key]
        for key in self.noncolliders:
            ls += self.noncolliders[key]
        self.reader.write(ls)
        with open(os.path.join('levels', 'player.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.player.serialize())

    def on_death(self):
        self.dead = True
        with open(os.path.join('levels', 'GameState.txt'), 'w') as f:
            f.write('0')
