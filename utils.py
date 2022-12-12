from random import randint

import pygame
import os
from numba import njit


def load_image(path, color_key=None):
    img = pygame.image.load(os.path.join('imgs', path))
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
