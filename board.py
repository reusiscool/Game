from pytmx.util_pygame import load_pygame
import os
from enum import Enum

from entity import Entity
from grassController import GrassController
from obs import Obs
from utils import draw_line, get_items, collides, vector_len


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
        self.reader = BoardReader()
        self.gc = GrassController(10, self.tile_size, 10)
        for o in self.reader.get_level(Level.Floor).tiles():
            x, y, surf = o
            self.add(Obs((x * self.tile_size, y * self.tile_size), 0, surf))
        for o in self.reader.get_level(Level.Boxes).tiles():
            x, y, _ = o
            self.add(Obs((x * self.tile_size, y * self.tile_size), self.tile_size))
        for o in self.reader.get_level(Level.Grass):
            self.gc.add_tile((o.x, o.y))
        self.boxes = self.get_boxes()

    def get_boxes(self):
        boxes = dict()
        level = self.reader.get_level(Level.Boxes)
        for tile in level.tiles():
            x, y, _ = tile
            if y not in boxes:
                boxes[y] = dict()
            boxes[y][x] = 1
        return boxes

    def add_entity(self, obj):
        x, y = obj.pos
        x //= self.tile_size
        y //= self.tile_size
        if y not in self.update_map:
            self.update_map[y] = {}
        if x not in self.update_map[y]:
            self.update_map[y][x] = []
        self.update_map[y][x].append(obj)
        self.add(obj)

    def add(self, obj: Entity):
        x, y = obj.pos
        x //= self.tile_size
        y //= self.tile_size
        if y not in self.collider_map:
            self.collider_map[y] = {}
        if x not in self.collider_map[y]:
            self.collider_map[y][x] = []
        self.collider_map[y][x].append(obj)

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

    def get_entities(self, pos, distance):
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


        sx, sy = entity1.pos
        sx //= self.tile_size
        sy //= self.tile_size


        px, py = entity2.pos
        px //= self.tile_size
        py //= self.tile_size

        for x, y in draw_line(sx, sy, px, py):
            if y not in self.boxes:
                continue
            if x not in self.boxes[y]:
                continue
            return False
        return True

    def update(self, pos, distance):
        for i in self.get_objects(pos, distance):
            i.update(self)
        self.gc.update()

    def render(self, surf, camera_x, camera_y, distance, pos_x, pos_y):
        ls = self.get_objects((pos_x, pos_y), distance) + self.gc.retrieve_surfs((pos_x, pos_y), distance)
        ls.sort(key=lambda o: sum(o.pos))
        for i in ls:
            i.render(surf, camera_x, camera_y)

