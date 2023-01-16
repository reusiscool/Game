from math import dist
from random import randint, choice
from scipy.spatial import Delaunay
from scipy.sparse.csgraph import minimum_spanning_tree
import os
import pygame
import numpy
import csv

from .rooms import Room, RoomType
from utils.utils import draw_line


class Layout:
    def __init__(self, lvl_num: int, size):
        self.corridors = {}
        self.size = size
        self.level_number = lvl_num
        self.map_ = [[]]
        self.rooms: dict[tuple, Room] = {}

    def generate(self):
        self.rooms = {}
        self.map_ = [[]]
        self.corridors = {}

        avg_room_size = 6

        room_num = (self.size // avg_room_size) ** 2 // 2

        ls = []
        for _ in range(room_num):
            while True:
                w = randint(avg_room_size - 1, avg_room_size + 1)
                h = randint(avg_room_size - 1, avg_room_size + 1)
                r = pygame.Rect(randint(0, self.size - 1 - w), randint(0, self.size - 1 - h), w, h)
                for i in ls:
                    if i.colliderect(r):
                        break
                else:
                    break
            ls.append(r)
        map_ = numpy.zeros((self.size, self.size), dtype=numpy.int8)
        for r in ls:
            r.move_ip(1, 1)
            r.inflate_ip(-1, -1)
            x1, y1 = r.topleft
            x2, y2 = r.bottomright
            map_[y1:y2, x1:x2] = 1

        points = numpy.array([i.center for i in ls])
        tri = Delaunay(points)
        mtrx = numpy.zeros((tri.npoints, tri.npoints))

        for con in tri.simplices:
            a, b, c = con
            mtrx[a, b] = mtrx[b, a] = dist(points[a], points[b])
            mtrx[c, b] = mtrx[b, c] = dist(points[c], points[b])
            mtrx[a, c] = mtrx[c, a] = dist(points[a], points[c])

        min_tree = minimum_spanning_tree(mtrx).toarray().astype(int)

        for con in tri.simplices:
            if randint(0, 10):
                continue
            a, b, c = con
            min_tree[a, b] = mtrx[b, a] = 1
            min_tree[c, b] = mtrx[b, c] = 1
            min_tree[a, c] = mtrx[c, a] = 1

        corridors = [[] for _ in range(len(min_tree))]

        for y in range(len(min_tree)):
            for x in range(len(min_tree)):
                if x - y > 0:
                    if min_tree[x, y] or min_tree[y, x]:
                        min_tree[y, x] = True
                        corridors[x].append(y)
                        corridors[y].append(x)
                else:
                    min_tree[y, x] = False

        for y, row in enumerate(min_tree):
            for x, val in enumerate(row):
                if not val:
                    continue
                x1, y1 = points[x]
                x2, y2 = points[y]
                for x5, y5 in draw_line(x1, y1, x2, y2):
                    map_[y5, x5] = 1
                for x5, y5 in draw_line(x1, y1 + 1, x2, y2 + 1):
                    map_[y5, x5] = 1

        self.map_ = map_
        self.corridors = corridors
        self._assign_rooms(ls, corridors)

    def add_room(self, room):
        self.rooms[room.rect.center] = room

    @property
    def room_list(self):
        return [self.rooms[key] for key in self.rooms]

    def get_rooms(self, pos, distance):
        """pos in tile coords"""
        px, py = pos
        for x in range(px - distance, px + distance + 1):
            for y in range(py - distance, py + distance + 1):
                if (x, y) in self.rooms:
                    yield self.rooms[(x, y)]

    @classmethod
    def read_from(cls, lvl_num):
        with open(os.path.join('.', 'save_files', 'layout.csv')) as f:
            reader = csv.reader(f)
            map_ = []
            for row in reader:
                if not row:
                    continue
                map_.append([int(i) for i in row])
        inst = Layout(lvl_num, len(map_))
        with open(os.path.join('.', 'save_files', 'rooms.csv')) as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                ls = [int(i) for i in row]
                inst.add_room(Room(pygame.Rect(ls[0], ls[1], ls[2], ls[3]), ls[4], RoomType(ls[5])))
        inst.map_ = map_
        return inst

    def _assign_rooms(self, room_rects: list[pygame.Rect], corridors: list[list[int]]):
        oneway = [RoomType.Weapon, RoomType.Shop, RoomType.DarkShop]
        twoway = [RoomType.Combat, RoomType.Null]
        res = [[] for _ in range(len(room_rects))]
        used = {}
        paired = set()
        for i, d in enumerate(corridors):
            if i in used:
                continue
            if len(d) == 1:
                rt = choice(oneway)
                used[i] = rt
                if rt == RoomType.DarkShop:
                    next_room = d[0]
                    used[next_room] = RoomType.Puzzle
                    paired.add((next_room, i))
            else:
                rt = choice(twoway)
                used[i] = rt
        keys = 2
        portaled = False
        for i, d in enumerate(corridors):
            if used[i] != RoomType.Null:
                continue
            if keys:
                used[i] = RoomType.Key
                keys -= 1
                continue
            if not portaled:
                used[i] = RoomType.Portal
                portaled = True
                continue
            used[i] = RoomType.Player
            break
        c = 100
        for key in used:
            c += 1
            res[key] = Room(room_rects[key], c, used[key])
        for roms in paired:
            r1, r2 = roms
            res[r1] = Room(room_rects[r1], c, used[r1])
            res[r2] = Room(room_rects[r2], c, used[r2])
        for rm in res:
            self.add_room(rm)

    def write(self):
        with open(os.path.join('.', 'save_files', 'layout.csv'), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.map_)
        with open(os.path.join('.', 'save_files', 'rooms.csv'), 'w') as f:
            writer = csv.writer(f)
            for i in self.rooms:
                room = self.rooms[i]
                writer.writerow((*tuple(room.rect), room.id_, room.type_.value))
