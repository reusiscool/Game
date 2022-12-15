from random import randint

import pygame
import os
from numba import njit


def load_image(*path, color_key=None):
    img = pygame.image.load(os.path.join('imgs', *path))
    if color_key is not None:
        img.set_colorkey(color_key)
    surf = img.convert()
    return surf


@njit
def normalize(x: int, y: int):
    a = x ** 2 + y ** 2
    if a == 0:
        return 0, 0
    k = a ** -0.5
    return x * k, y * k


def draw_line(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy

    ans = set()

    while True:
        ans.add((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error = error + dy
            x0 = x0 + sx
        if e2 <= dx:
            if y0 == y1:
                break
            error = error + dx
            y0 = y0 + sy
    return ans


def get_items(self, pos, distance, map_):
    x, y = pos
    stx = int((x - distance) // self.tile_size)
    endx = int((x + distance) // self.tile_size)
    sty = int((y - distance) // self.tile_size)
    endy = int((y + distance) // self.tile_size)
    ls = []
    for ny in range(sty, endy + 1):
        if ny not in map_:
            continue
        for nx in range(stx, endx + 1):
            if nx not in map_[ny]:
                continue
            for b in map_[ny][nx]:
                ls.append(b)
    return ls


def vector_len(vec):
    return (vec[0] ** 2 + vec[1] ** 2) ** 0.5


def vector_angle(vec1, vec2):
    """ vec1: (x0, y0); vec2: (x1, y1) - returns cosine of angle between vectors"""
    a = (vector_len(vec1) * vector_len(vec2))
    if a == 0:
        return -1
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / a


def collides(p1, p2, left, bottom, width, height):
    # vx = △x, vy = △y
    right = left + width
    top = bottom + height
    x, y = p1
    x2, y2 = p2
    vx = x2 - x
    vy = y2 - y
    p = [-vx, vx, -vy, vy]
    q = [x - left, right - x, y - bottom, top - y]
    u1 = -float('inf')
    u2 = float('inf')

    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return False
        else:
            t = q[i] / p[i]
            if p[i] < 0 and u1 < t:
                u1 = t
            elif p[i] > 0 and u2 > t:
                u2 = t

    if u1 > u2 or u1 > 1 or u1 < 0:
        return False
    return True
