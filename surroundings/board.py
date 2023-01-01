from random import randint
from typing import Protocol

from enemies.baseEnemy import EnemyStats
from loot.baseLoot import BaseLoot
from weapons.baseProjectile import BaseProjectile
from enemies.enemy import Enemy
from enemies.enemyAI import EnemyAI
from surroundings.grassController import GrassController
from .layout import Layout
from .levelReader import LevelReader
from .obs import Obs, Wall
from loot.keyItemLoot import KeyItemLoot
from enemies.shootingEnemy import ShootingEnemy
from weapons.sword import Sword, SwordStats
from utils.utils import load_image
from loot.weaponLoot import WeaponLoot


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
    def __init__(self, tile_size, player, update_distance, render_distance):
        self.render_distance = render_distance
        self.update_distance = update_distance
        self.player = player
        self.tile_size = tile_size
        self.collider_map: dict[tuple, list[CollisionEntity]] = {}
        self.update_map: dict[tuple, list[UpdatableEntity]] = {}
        self.enemy_map: dict[tuple, list[UpdatableEntity]] = {}
        self.loot: dict[tuple, list[BaseLoot]] = {}
        self.enemyAI = EnemyAI()
        self.floor_map: dict[tuple, list[Obs]] = {}
        self.projectiles: list[BaseProjectile] = []
        self.reader = LevelReader(Layout('1', 40))
        self.gc = GrassController(10, self.tile_size, 10)
        keyx, keyy = self.reader.key_room
        keyx *= self.tile_size
        keyy *= self.tile_size
        self.add_loot(KeyItemLoot((keyx, keyy), 0))
        for x, y, surf in self.reader.get_floor():
            obj = Obs((x * self.tile_size, y * self.tile_size), 0, surf)
            self.add_item(obj, self.floor_map)
        for x, y, surf in self.reader.get_walls():
            self.add_item(Wall((x * self.tile_size, y * self.tile_size), 0, surf), self.collider_map)
            self.add(Obs((x * self.tile_size, y * self.tile_size), self.tile_size))
        for x, y in self.reader.get_enemies():
            if randint(0, 1):
                es = EnemyStats((x * self.tile_size + randint(0, 30) - 15, y * self.tile_size, 5),
                                3, 70, 70, 250, 150, 20, 20, 100)
                en = ShootingEnemy([load_image('grass.jpg')], es)
            else:
                es = EnemyStats((x * self.tile_size + randint(0, 30) - 15, y * self.tile_size, 5),
                                3, 70, 70, 250, 60, 15, 20)
                en = Enemy([load_image('grass.jpg')], es)
            en.nudge()
            self.add_enemy(en)
        for x, y in self.reader.weapons:
            x *= self.tile_size
            y *= self.tile_size
            sword_stats = SwordStats(50, 100, 30, 20, 0)
            ls = [load_image('sword', 'sword.png', color_key='white')]
            sw = Sword(ls, sword_stats)
            self.add_loot(WeaponLoot((x, y), ls, sw))
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

    def add_loot(self, obj: BaseLoot):
        self.add_item(obj, self.loot)

    def pop_loot(self, obj):
        self.pop_item(obj, self.loot)

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
        self.enemyAI.update(self)
        for i in self.get_items(self.player.pos, self.update_distance, self.loot):
            i.update(self)
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
                if pos in self.loot:
                    ls += self.loot[pos]
                ls.sort(key=lambda o: sum(o.pos))
                for i in ls:
                    i.render(surf, camera_x, camera_y)

