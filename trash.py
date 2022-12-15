from utils import collides
import pygame

r = pygame.Rect(15, -40, 25, 80)
print(collides((10, 10), (20, 0), *r.topleft, *r.size))
