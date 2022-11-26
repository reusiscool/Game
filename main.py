import sys
import pygame

import converters
from camera import Camera
from grass import Grass
from player import Player
from maps import ls_obstacles
from entity import Entity
from particles import Particle


class App:
    def __init__(self, size=(1600, 900), obj_ls=None):
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.display = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.camera = Camera([0, 0])
        self.player = Player((0, 0), self.add_particle)
        self.ls = [Entity((i * 40, i * 20)) for i in range(1, 10)]
        self.parts: list[Particle] = []
        obj_ls += [i.rect for i in self.ls]
        gr = pygame.image.load('imgs\\grass.jpg').convert()
        gr.set_colorkey((255, 255, 255))
        self.grass = [Grass((-30, -30), gr)]

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

    def render(self):
        for i in self.ls:
            i.render(self.display, *self.camera.pos)
        for i in range(len(self.parts) - 1, -1, -1):
            if not self.parts[i].render(self.display, *self.camera.pos):
                self.parts.pop(i)
        self.player.render(self.display, *self.camera.pos)
        for i in self.grass:
            i.render(self.display, *self.camera.pos)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            x, y = self.player.get_coords()
            x1, y1 = converters.mum_convert(x, y)
            self.camera.adjust((x1, y1), self.display.get_size())
            self.display.fill('black')
            self.fps_counter()
            self.check_controls()
            self.render()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    app = App(obj_ls=ls_obstacles)
    app.run()
