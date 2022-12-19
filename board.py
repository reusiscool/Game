from pytmx.util_pygame import load_pygame
import os
from enum import Enum

from entity import Entity
from grassController import GrassController
from obs import Obs
from utils import get_items, collides, vector_len, add_item


class Level(Enum):
    Floor = 'Floor'
    Grass = 'Grass'
    Boxes = 'Boxes'


class BoardReader:
    def __init__(self):
        self.reader = load_pygame(os.path.join('tiled', 'tsxFiles', 'bigmap.tmx'))

    def get_level(self, level: Level):
        return self.reader.get_layer_by_name(level.value)


class Board:
    def __init__(self, tile_size, player):
        self.player = player
        self.tile_size = tile_size
        self.collider_map: dict[int, dict[int, list[Entity]]] = {}
        self.update_map: dict[int, dict[int, list[Entity]]] = {}
        self.floor_map: dict[int, dict[int, list[Entity]]] = {}
        self.reader = BoardReader()
        self.gc = GrassController(10, self.tile_size, 10)
        self.projectiles = []
        for o in self.reader.get_level(Level.Floor).tiles():
            x, y, surf = o
            obj = Obs((x * self.tile_size, y * self.tile_size), 0, surf)
            add_item(self, obj, self.floor_map)
        for o in self.reader.get_level(Level.Boxes).tiles():
            x, y, _ = o
            self.add(Obs((x * self.tile_size, y * self.tile_size), self.tile_size))
        for o in self.reader.get_level(Level.Grass):
            self.gc.add_tile((o.x, o.y))

    def get_boxes(self):
        boxes = dict()
        level = self.reader.get_level(Level.Boxes)
        for tile in level.tiles():
            x, y, _ = tile
            if y not in boxes:
                boxes[y] = dict()
            boxes[y][x] = 1
        return boxes

    def add_projectile(self, obj):
        self.projectiles.append(obj)

    def pop_projectile(self, obj):
        self.projectiles.remove(obj)

    def add_entity(self, obj):
        add_item(self, obj, self.update_map)
        self.add(obj)

    def add(self, obj: Entity):
        add_item(self, obj, self.collider_map)

    def pop(self, obj):
        x, y = obj.pos
        x //= self.tile_size
        y //= self.tile_size
        if y not in self.collider_map:
            return
        if x not in self.collider_map[y]:
            return
        self.collider_map[y][x].remove(obj)

    def pop_entity(self, obj):
        self.pop(obj)
        x, y = obj.pos
        x //= self.tile_size
        y //= self.tile_size
        if y not in self.update_map:
            return
        if x not in self.update_map[y]:
            return
        self.update_map[y][x].remove(obj)

    def get_entities(self, pos, distance) -> list[Entity]:
        return get_items(self, pos, distance, self.update_map)

    def get_objects(self, pos, distance) -> list[Entity]:
        return get_items(self, pos, distance, self.collider_map)

    def has_clear_sight(self, entity1: Entity, entity2: Entity = None) -> bool:

        if entity2 is None:
            entity2 = self.player

        cx, cy = (entity1.x + entity2.x) / 2, (entity1.y + entity2.y) / 2
        d = vector_len((entity1.x - entity2.x, entity1.y - entity2.y))
        p1, p2 = entity2.pos, entity1.pos

        for obj in self.get_objects((cx, cy), d):
            if obj in (entity1, entity2):
                continue
            if collides(p1, p2, *obj.rect.topleft, *obj.rect.size):
                return False
        return True

    def update(self, pos, distance):
        for proj in self.projectiles:
            proj.update(self)
        for i in self.get_objects(pos, distance):
            i.update(self)
        self.gc.update()

    def render(self, surf, camera_x, camera_y, distance, pos_x, pos_y):
        for floor in get_items(self, (pos_x, pos_y), distance, self.floor_map):
            floor.render(surf, camera_x, camera_y)
        ls = self.get_objects((pos_x, pos_y), distance) + self.gc.retrieve_surfs((pos_x, pos_y), distance)
        ls += self.projectiles
        ls.sort(key=lambda o: sum(o.pos))
        for i in ls:
            i.render(surf, camera_x, camera_y)

