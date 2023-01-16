import os
from random import randint, choice
import pygame
import csv

from enemies.dashEnemy import DashEnemy
from enemies.shootingEnemy import ShootingEnemy
from interactables.darkShop import DarkShop
from interactables.portal import Portal
from interactables.shop import Shop
from loot.keyItemLoot import KeyItemLoot
from enemies.baseEnemy import EnemyStats
from loot.moneyLoot import MoneyLoot
from puzzles.basePuzzle import BasePuzzle
from surroundings.trap import Trap, TrapStats
from surroundings.rooms import Room, RoomType
from utils.savingConst import SavingConstants
from puzzles.ticPuzzle import TicTacToePuzzle
from puzzles.liarPuzzle import LiarPuzzle
from weapons.sword import Sword
from interactables.weaponLoot import WeaponLoot


class EntityGen:
    def __init__(self, level_number: int, tile_size: int):
        self.tile_size = tile_size
        self.level_number = level_number
        self.enemies = []
        self.noncolliders = []
        self.constants = SavingConstants()
        self.constants.level = level_number

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
                if randint(0, self.constants.trap_chance[self.level_number - 1]):
                    continue
                dx, dy = x * self.tile_size, y * self.tile_size
                ts = TrapStats(dmg, cd, pygame.Rect(dx, dy, self.tile_size, self.tile_size), up_cd)
                self.noncolliders.append(Trap(ts))

    def _rarity_roll(self):
        roll = randint(1, 100)
        if roll > 95:
            rarity = 3
        elif roll > 80:
            rarity = 2
        elif roll > 50:
            rarity = 1
        else:
            rarity = 0
        return rarity

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
                reward = []
                for _ in range(3):
                    if randint(0, 1):
                        reward.append(MoneyLoot(pos, self.constants.gold_drop[self.level_number - 1]))
                self.noncolliders.append(puzzle(pos, room.id_, reward))
            elif room.type_ == RoomType.Weapon:
                self.noncolliders.append(WeaponLoot(room.pos_to_tiles(self.tile_size),
                                                    Sword.generate(self._rarity_roll(),
                                                                   self.level_number)))
            elif room.type_ == RoomType.Portal:
                self.noncolliders.append(Portal(room.pos_to_tiles(self.tile_size)))
            elif room.type_ == RoomType.Shop:
                self.noncolliders.append(Shop(room.pos_to_tiles(self.tile_size),
                                              self._rarity_roll(),
                                              self.level_number))
            elif room.type_ == RoomType.DarkShop:
                self.noncolliders.append(DarkShop(room.pos_to_tiles(self.tile_size),
                                                  self._rarity_roll(), [room.id_],
                                                  self.level_number))

    def write(self, entity_list):
        ls = []
        for entity in entity_list:
            if self.constants.contains(type(entity)) or isinstance(entity, BasePuzzle):
                ls.append(entity.serialize())
        with open(os.path.join('save_files', 'entities.csv'), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(ls)

    @classmethod
    def read(cls, number: int, tile_size: int):
        instance = cls(number, tile_size)
        instance.constants.level = number
        with open(os.path.join('save_files', 'entities.csv')) as f:
            reader = csv.reader(f)
            for line in reader:
                if not line:
                    continue
                type_ = instance.constants.get_type(int(line[0]))
                if type_ in (Trap, BasePuzzle):
                    instance.noncolliders.append(type_.read(line, number))
                elif type_ in (DashEnemy, ShootingEnemy):
                    instance.enemies.append(type_.read(line, number))
                else:
                    ent = instance.constants.load(line)
                    instance.noncolliders.append(ent)
        return instance
