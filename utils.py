import pygame
import os


def load_image(path, color_key=None):
    img = pygame.image.load(os.path.join('imgs', path))
    if color_key is not None:
        img.set_colorkey(color_key)
    surf = img.convert()
    return surf
