import pygame

import converters
from maps import ls_obstacles


class Player:
    radius = 10

    def __init__(self, pos, col_fn):
        self.collision_call = col_fn
        self.x = pos[0]
        self.y = pos[1]
        self.width = 5
        self.height = 5
        self.texture = pygame.Surface([self.radius * 2] * 2)
        self.texture.set_colorkey('black')
        self.particle_time = 20
        self.paint()

    @property
    def rect(self):
        return pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def paint(self):
        pygame.draw.circle(self.texture, 'red', (self.radius, self.radius), self.radius)

    def move(self, x, y):
        self.x += x
        self._move_x(x)
        self.y += y
        self._move_y(y)
        if not self.particle_time:
            self.collision_call(self.x, self.y)
            self.collision_call(self.x, self.y)
            self.particle_time = 5

    def _move_x(self, dx):
        if not dx:
            return
        rect = self.rect
        for obj in ls_obstacles:
            if rect.colliderect(obj):
                if dx > 0:
                    rect.right = obj.left
                else:
                    rect.left = obj.right
                self.x = rect.x
                # if not self.collision_timer:
                #     for _ in range(1):
                #         self.collision_call(self.x, self.y)
                #     self.collision_timer = 0

    def _move_y(self, dy):
        if not dy:
            return
        rect = self.rect
        for obj in ls_obstacles:
            if rect.colliderect(obj):
                if dy > 0:
                    rect.bottom = obj.top
                else:
                    rect.top = obj.bottom
                self.y = rect.y
                # if not self.collision_timer:
                #     for _ in range(1):
                #         self.collision_call(self.x, self.y)
                #     self.collision_timer = 0

    def get_coords(self):
        return self.x, self.y
        
    def render(self, surf: pygame.Surface, camera_x, camera_y):
        self.particle_time = max(0, self.particle_time - 1)
        x, y = converters.mum_convert(*self.get_coords())
        off_x = self.texture.get_width() // 2
        off_y = self.texture.get_height()
        surf.blit(self.texture, (x - camera_x - off_x, y - camera_y - off_y + 2))
