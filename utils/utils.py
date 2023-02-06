import pygame
import os
from numba import njit
import numpy
from math import cos, sin, radians
from typing import Iterable

from .singleton import Singleton


class LoadMemory(metaclass=Singleton):
    def __init__(self):
        self.d = {}


def load_image(*path, color_key=None):
    memory = LoadMemory()
    hash_ = (path, color_key)
    if hash_ in memory.d:
        return memory.d[hash_]
    img = pygame.image.load(os.path.join('.', 'imgs', *path))
    if color_key is not None:
        img.set_colorkey(color_key)
    surf = img.convert()
    memory.d[hash_] = surf
    return surf


@njit
def normalize(x: int, y: int):
    a = x ** 2 + y ** 2
    if a == 0:
        return 0, 0
    k = a ** -0.5
    return x * k, y * k


def is_left(line_point1, line_point2, point):
    return (line_point2[0] - line_point1[0]) * (point[1] - line_point1[1]) >\
           (line_point2[1] - line_point1[1]) * (point[0] - line_point1[0])


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


@njit
def vector_len(vec):
    return (vec[0] ** 2 + vec[1] ** 2) ** 0.5


@njit
def vector_angle(vec1, vec2):
    """ vec1: (x0, y0); vec2: (x1, y1) - returns cosine of angle between vectors"""
    a = (vector_len(vec1) * vector_len(vec2))
    if a == 0:
        return -1
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / a


@njit
def collides(p1, p2, left: int, bottom: int, width: int, height: int):
    """
    Checks whether line segment and rect collide
    :param p1: first point of line segment
    :param p2: second point of line segment
    :param left: x of rect
    :param bottom: top in pygame coords
    :param width: width of rect
    :param height: height of rect
    :return: Boolean
    """
    # vx = △x, vy = △y
    right = left + width
    top = bottom + height
    x, y = p1
    x2, y2 = p2
    vx = x2 - x
    vy = y2 - y
    p = [-vx, vx, -vy, vy]
    q = [x - left, right - x, y - bottom, top - y]
    u1 = -10_000
    u2 = 10_000

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


def rotate(vec2: Iterable, angle: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """
    Rotates point around (0; 0)
    :param vec2: point (x, y)
    :param angle: degrees
    :return: coords of two points
    """
    vec2 = numpy.array(vec2)
    rad = radians(angle)
    cosa = cos(rad)
    sina = sin(rad)
    turn_mat1 = numpy.array([[cosa, -sina], [sina, cosa]])
    turn_mat2 = numpy.array([[cosa, sina], [-sina, cosa]])
    return vec2 @ turn_mat1, vec2 @ turn_mat2


def draw_rect_line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    s = set()
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    for x in range(x1, x2 + 1):
        s.add((x, y1))
    if y1 < y2:
        for y in range(y1, y2 + 1):
            s.add((x2, y))
    else:
        for y in range(y2, y1 + 1):
            s.add((x2, y))
    return s


def draw_rect_line2(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    s = set()
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    for x in range(x1, x2 + 1):
        s.add((x, y2))
    if y1 < y2:
        for y in range(y1, y2 + 1):
            s.add((x1, y))
    else:
        for y in range(y2, y1 + 1):
            s.add((x1, y))
    return s


collides((0, 1), (1, 0), 10, 10, 10, 10)
