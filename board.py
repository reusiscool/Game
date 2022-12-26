from random import randint
from typing import Protocol

from baseProjectile import BaseProjectile
from enemy import Enemy
from entity import Entity
from grassController import GrassController
from levelReader import LevelReader
from obs import Obs, Wall
from utils import collides, vector_len, load_image
from layout import Layout


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
    def __init__(self, tile_size, player, simulation_distance, render_distance):
        self.render_distance = render_distance
        self.update_distance = simulation_distance
        self.player = player
        self.tile_size = tile_size
        self.collider_map: dict[tuple, list[CollisionEntity]] = {}
        self.update_map: dict[tuple, list[UpdatableEntity]] = {}
        self.floor_map: dict[tuple, list[Obs]] = {}
        self.projectiles: list[BaseProjectile] = []
        self.reader = LevelReader(Layout('1', 40))
        self.gc = GrassController(10, self.tile_size, 10)
        for x, y, surf in self.reader.get_floor():
            obj = Obs((x * self.tile_size, y * self.tile_size), 0, surf)
            self.add_item(obj, self.floor_map)
        for x, y, surf in self.reader.get_walls():
            self.add_item(Wall((x * self.tile_size, y * self.tile_size), 0, surf), self.collider_map)
            self.add(Obs((x * self.tile_size, y * self.tile_size), self.tile_size))
        for x, y in self.reader.get_enemies():
            en = Enemy((x * self.tile_size + randint(0, 30) - 15, y * self.tile_size), 5, [load_image('grass.jpg')], 5, health=100)
            en.nudge()
            self.add_entity(en)
        player.x, player.y = self.reader.player_room
        player.x *= self.tile_size
        player.y *= self.tile_size

    def add_item(self, obj, map_: dict[tuple, list]):
        pos = obj.tile_pos(self.tile_size)
        if pos not in map_:
            map_[pos] = []
        map_[pos].append(obj)

    def get_items(self, pos, distance, map_: dict[tuple, list]):
        x, y = pos
        ls = []
        for ny in range(int((y - distance) // self.tile_size), int((y + distance) // self.tile_size) + 1):
            for nx in range(int((x - distance) // self.tile_size), int((x + distance) // self.tile_size) + 1):
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

    def add_projectile(self, obj):
        self.projectiles.append(obj)

    def pop_projectile(self, obj):
        self.projectiles.remove(obj)

    def add_entity(self, obj: UpdatableEntity):
        self.add_item(obj, self.update_map)
        self.add(obj)

    def add(self, obj: CollisionEntity):
        self.add_item(obj, self.collider_map)

    def pop(self, obj: CollisionEntity):
        self.pop_item(obj, self.collider_map)

    def pop_entity(self, obj: UpdatableEntity):
        self.pop(obj)
        self.pop_item(obj, self.update_map)

    def get_entities(self, pos, distance) -> list[UpdatableEntity]:
        return self.get_items(pos, distance, self.update_map)

    def get_objects(self, pos, distance) -> list[CollisionEntity]:
        return self.get_items(pos, distance, self.collider_map)

    def has_clear_sight(self, entity1: Entity, entity2: Entity = None) -> bool:
        if entity2 is None:
            entity2 = self.player

        cx, cy = (entity1.x + entity2.x) / 2, (entity1.y + entity2.y) / 2
        d = vector_len((entity1.x - entity2.x, entity1.y - entity2.y)) / 2
        p1, p2 = entity1.pos, entity2.pos
        p1 = tuple(int(i) for i in p1)
        p2 = tuple(int(i) for i in p2)

        for obj in self.get_objects((cx, cy), d):
            if obj in (entity1, entity2):
                continue
            if collides(p1, p2, *map(int, (*obj.rect.topleft, *obj.rect.size))):
                return False
        return True

    def update(self):
        for i in self.projectiles:
            i.update(self)
        for i in self.get_entities(self.player.pos, self.update_distance):
            i.update(self)
        self.gc.update()

    def render(self, surf, camera_x, camera_y, x, y):
        for floor in self.get_items((x, y), self.render_distance, self.floor_map):
            floor.render(surf, camera_x, camera_y)
        stx = int((x - self.render_distance) // self.tile_size)
        endx = int((x + self.render_distance) // self.tile_size)
        sty = int((y - self.render_distance) // self.tile_size)
        endy = int((y + self.render_distance) // self.tile_size)
        proj_map = {}
        for i in self.projectiles:
            self.add_item(i, proj_map)
        for ny in range(sty, endy + 1):
            for nx in range(stx, endx + 1):
                ls = []
                pos = (nx, ny)
                if pos in self.collider_map:
                    ls += self.collider_map[pos]
                if pos in proj_map:
                    ls += proj_map[pos]
                ls.sort(key=lambda o: sum(o.pos))
                for i in ls:
                    i.render(surf, camera_x, camera_y)

