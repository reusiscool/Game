import os
from random import randint, choice
import pygame
import csv

from enemies.dashEnemy import DashEnemy
from enemies.shootingEnemy import ShootingEnemy
from interactables.portal import Portal
from interactables.shop import Shop
from loot.healItemLoot import HealItemLoot
from loot.healthLoot import HealthLoot
from loot.keyItemLoot import KeyItemLoot
from enemies.baseEnemy import EnemyStats
from loot.manaItemLoot import ManaItemLoot
from loot.manaLoot import ManaLoot
from puzzles.basePuzzle import BasePuzzle
from surroundings.trap import Trap, TrapStats
from surroundings.rooms import Room, RoomType
from utils.savingConst import SavingConstants
from puzzles.ticPuzzle import TicTacToePuzzle
from puzzles.liarPuzzle import LiarPuzzle
from weapons.sword import Sword, SwordStats
from interactables.weaponLoot import WeaponLoot


class EntityGen:
    def __init__(self, level_number: int, tile_size: int):
        self.tile_size = tile_size
        self.level_number = level_number
        self.enemies = []
        self.noncolliders = []
        self.constants = SavingConstants()
        self._loads = {
            self.constants.get_const(ShootingEnemy): lambda x: self._load_enemy(x),
            self.constants.get_const(DashEnemy): lambda x: self._load_enemy(x),
            self.constants.get_const(WeaponLoot): lambda x: self._load_weapon(x),
            self.constants.get_const(KeyItemLoot): lambda x: self._load_key(x),
            self.constants.get_const(Trap): lambda x: self._load_trap(x),
            self.constants.get_const(BasePuzzle): lambda x: self._load_puzzle(x),
            self.constants.get_const(Portal): lambda x: self._load_portal(x),
            self.constants.get_const(HealthLoot): lambda x: self._load_mana_health(x, HealthLoot),
            self.constants.get_const(ManaLoot): lambda x: self._load_mana_health(x, ManaLoot),
            self.constants.get_const(ManaItemLoot): lambda x: self._load_mana_health(x, ManaItemLoot),
            self.constants.get_const(HealItemLoot): lambda x: self._load_mana_health(x, HealItemLoot)
        }

    def _gen_enemies(self, room):
        for i in range(self.constants.enemies_per_room[self.level_number - 1]
                       + randint(0, 1)):
            enemy = choice((ShootingEnemy, DashEnemy))
            dx, dy = room.pos_to_tiles(self.tile_size)
            speed, health, *stats = self.constants.get_stats(enemy, self.level_number)
            es = EnemyStats((dx + i * 10, dy + i * 10, 10), speed, health, health, *stats)
            enemy = enemy(es)
            enemy.nudge()
            self.enemies.append(enemy)

    def _gen_traps(self, room):
        dmg, cd, up_cd = self.constants.get_stats(Trap, self.level_number)
        for x in range(room.rect.x, room.rect.right):
            for y in range(room.rect.y, room.rect.bottom):
                if randint(0, 3):
                    continue
                dx, dy = x * self.tile_size, y * self.tile_size
                ts = TrapStats(dmg, cd, pygame.Rect(dx, dy, self.tile_size, self.tile_size), up_cd)
                self.noncolliders.append(Trap(ts))

    def generate(self, rooms: list[Room]):
        c = 0
        trap_rooms = (RoomType.Null, RoomType.Puzzle)
        for room in rooms:
            if room.type_ in trap_rooms:
                self._gen_traps(room)
            if room.type_ == RoomType.Key:
                self.noncolliders.append(KeyItemLoot(room.pos_to_tiles(self.tile_size), c))
                c += 1
            elif room.type_ == RoomType.Combat:
                self._gen_enemies(room)
            elif room.type_ == RoomType.Puzzle:
                puzzle = choice((TicTacToePuzzle, LiarPuzzle))
                pos = room.pos_to_tiles(self.tile_size)
                self.noncolliders.append(puzzle(pos, room.id_))
            elif room.type_ == RoomType.Weapon:
                sws = self.constants.get_stats(Sword, self.level_number)
                sws = SwordStats(*sws)
                self.noncolliders.append(WeaponLoot(room.pos_to_tiles(self.tile_size), Sword(sws)))
            elif room.type_ == RoomType.Portal:
                self.noncolliders.append(Portal(room.pos_to_tiles(self.tile_size)))
            elif room.type_ == RoomType.Shop:
                self.noncolliders.append(Shop(room.pos_to_tiles(self.tile_size), 0, self.level_number))

    def write(self, entity_list):
        ls = []
        for entity in entity_list:
            if self.constants.contains(type(entity)) or isinstance(entity, BasePuzzle):
                ls.append(entity.serialize())
        with open(os.path.join('levels', 'entities.csv'), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(ls)

    def _load_enemy(self, line):
        enemy = self.constants.get_type(int(line[0]))
        pos = eval(line[1])
        cur_hp = int(line[2])
        speed, *stats = self.constants.get_stats(enemy, self.level_number)
        es = EnemyStats((*pos, 10),
                        speed, cur_hp, *stats)
        enemy = enemy(es)
        self.enemies.append(enemy)

    def _load_trap(self, line):
        pos = eval(line[1])
        dmg, cd, up_cd = self.constants.get_stats(Trap, self.level_number)
        ts = TrapStats(dmg, cd, pygame.Rect(*pos, self.tile_size, self.tile_size), up_cd)
        self.noncolliders.append(Trap(ts))

    def _load_key(self, line):
        id_ = int(line[1])
        pos = eval(line[2])
        self.noncolliders.append(KeyItemLoot(pos, id_))

    def _load_weapon(self, line):
        dmg = int(line[1])
        rng = int(line[2])
        angle = int(line[3])
        cd = int(line[4])
        knock = int(line[5])
        pos = eval(line[6])
        sws = SwordStats(dmg, rng, angle, cd, knock)
        self.noncolliders.append(WeaponLoot(pos, Sword(sws)))

    def _load_mana_health(self, line, type_):
        pos = eval(line[1])
        amount = int(line[2])
        self.noncolliders.append(type_(pos, amount))

    def _load_portal(self, line):
        locks = list(eval(line[1]))
        pos = eval(line[2])
        portal = Portal(pos, locks)
        self.noncolliders.append(portal)

    def _load_puzzle(self, line):
        id_ = int(line[1])
        pos = eval(line[2])
        puzzle = choice((TicTacToePuzzle, LiarPuzzle))
        self.noncolliders.append(puzzle(pos, id_))

    @classmethod
    def read(cls, number: int, tile_size: int):
        instance = cls(number, tile_size)
        with open(os.path.join('levels', 'entities.csv')) as f:
            reader = csv.reader(f)
            for line in reader:
                if not line:
                    continue
                ind = int(line[0])
                instance._loads[ind](line)
        return instance
