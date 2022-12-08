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
