import pygame


def load_image(path, color_key=None):
    img = pygame.image.load(path)
    if color_key is not None:
        img.set_colorkey(color_key)
    surf = img.convert()
    return surf
