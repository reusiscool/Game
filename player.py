import pygame
import converters
from entity import Entity


class Player(Entity):
    radius = 10

    def __init__(self, pos, hitbox_size, image):
        super().__init__(pos, hitbox_size, image)

    def render(self, surf: pygame.Surface, camera_x, camera_y):
        x, y = converters.mum_convert(*self.get_coords())
        off_x = self.image.get_width() // 2
        off_y = self.image.get_height()
        surf.blit(self.image, (x - camera_x - off_x, y - camera_y - off_y + self.hitbox_size // 2))
