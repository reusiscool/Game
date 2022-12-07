import random
import sys
import pygame

from converters import mum_convert
from board import Board
from camera import Camera
from grass import Grass
from grassController import GrassController
from player import Player
from obs import Obs
from particles import Particle
from utils import load_image


class App:
    def __init__(self, size=(1600, 900)):
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.W, self.H = size
        self.screen = pygame.display.set_mode(size)
        self.display = pygame.Surface((size[0] // 2, size[1] // 2))
        self.clock = pygame.time.Clock()
        self.camera = Camera([0, 0])
        self.player = Player((0, 0), 5, load_image('grass.png'))
        self.parts: list[Particle] = []
        self.board = Board(50)
        for i in range(3, 10):
            self.board.add(Obs((i * 40, i * 20)))
        self.board.add(self.player)
        # for i in range(10):
        #     for j in range(10):
        #         self.gc.add_tile((i * 10, j * 10))

        # all_grass = [load_image(f'grass_{i}.png', 'black') for i in range(6)]
        # self.grass = []
        # for i in range(10):
        #     for j in range(10):
        #         self.grass.append(Grass((i * 4, j * 4), random.choice(all_grass)))

    def check_controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
            self.player.move_coords(4, 4)
        if keys[pygame.K_w]:
            self.player.move_coords(-4, -4)
        if keys[pygame.K_d]:
            self.player.move_coords(4, -4)
        if keys[pygame.K_a]:
            self.player.move_coords(-4, 4)

    def add_particle(self, x, y):
        self.parts.append(Particle([x, y]))

    def fps_counter(self):
        fps_t = self.font.render(str(int(self.clock.get_fps())), True, 'Blue')
        self.display.blit(fps_t, (0, 0))

    def update(self):
        self.board.update(self.player.pos, 500)
        # for i in self.grass:
        #     i.update(self.player.get_coords())
        # self.gc.update()
        # self.player.update(self.board)

    def render(self):
        nx, ny = self.camera.pos
        nx, ny = mum_convert(nx + self.W // 2, ny + self.H // 2)
        self.board.render(self.display, *self.camera.pos, 500, nx, ny)
        # for i in self.board.map:
        #     i.render(self.display, *self.camera.pos)
        # for i in range(len(self.parts) - 1, -1, -1):
        #     if not self.parts[i].render(self.display, *self.camera.pos):
        #         self.parts.pop(i)
        # for i in self.grass:
        #     i.render(self.display, *self.camera.pos)
        # for i in self.gc.retrieve_surfs():
        #     i.render(self.display, *self.camera.pos)
        # self.player.render(self.display, *self.camera.pos)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            x, y = self.player.pos
            x1, y1 = mum_convert(x, y)
            self.camera.adjust((x1, y1), self.display.get_size())
            self.update()
            self.display.fill((250, 80, 100))
            self.fps_counter()
            self.check_controls()
            self.render()
            pygame.draw.circle(self.display, 'yellow', (self.W // 4, self.H // 4), 3)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
