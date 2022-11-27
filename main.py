import random
import sys
import pygame

import converters
from camera import Camera
from grass import Grass
from player import Player
from maps import ls_obstacles
from entity import Entity
from particles import Particle
from utils import load_image


class App:
    def __init__(self, size=(1600, 900), obj_ls=None):
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.screen = pygame.display.set_mode(size)
        self.display = pygame.Surface((size[0] // 2, size[1] // 2))
        self.clock = pygame.time.Clock()
        self.camera = Camera([0, 0])
        self.player = Player((-20, 0), self.add_particle)
        self.ls = [Entity((i * 40, i * 20)) for i in range(1, 10)]
        self.parts: list[Particle] = []
        all_grass = [load_image(f'imgs\\grass_{i}.png', 'black') for i in range(6)]
        obj_ls += [i.rect for i in self.ls]
        self.grass = []
        for i in range(20):
            for j in range(5):
                self.grass.append(Grass((i*2.5 - 0, j*2.5 - 0), random.choice(all_grass)))

    def check_controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
            self.player.move(4, 4)
        if keys[pygame.K_w]:
            self.player.move(-4, -4)
        if keys[pygame.K_d]:
            self.player.move(4, -4)
        if keys[pygame.K_a]:
            self.player.move(-4, 4)

    def add_particle(self, x, y):
        self.parts.append(Particle([x, y]))

    def fps_counter(self):
        fps_t = self.font.render(str(int(self.clock.get_fps())), True, 'Blue')
        self.display.blit(fps_t, (0, 0))

    def update(self):
        for i in self.grass:
            i.update(self.player.get_coords())

    def render(self):
        for i in self.ls:
            i.render(self.display, *self.camera.pos)
        for i in range(len(self.parts) - 1, -1, -1):
            if not self.parts[i].render(self.display, *self.camera.pos):
                self.parts.pop(i)
        for i in self.grass:
            i.render(self.display, *self.camera.pos)
        self.player.render(self.display, *self.camera.pos)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            x, y = self.player.get_coords()
            x1, y1 = converters.mum_convert(x, y)
            self.camera.adjust((x1, y1), self.display.get_size())
            self.update()
            self.display.fill((250, 80, 100))
            self.fps_counter()
            self.check_controls()
            self.render()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    app = App(obj_ls=ls_obstacles)
    app.run()
