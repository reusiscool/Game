import sys
import pygame

from converters import mum_convert, back_convert
from board import Board
from camera import Camera
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
        self.player = Player((0, 0), 5, load_image('grass.png'), 4)
        self.parts: list[Particle] = []
        self.board = Board(30)
        for i in range(3, 10):
            self.board.add(Obs((i * 40, i * 20), 40))
        self.board.add(self.player)

    def check_controls(self):
        keys = pygame.key.get_pressed()
        s = keys[pygame.K_s]
        d = keys[pygame.K_d]
        w = keys[pygame.K_w]
        a = keys[pygame.K_a]
        if keys[pygame.K_LSHIFT]:
            self.player.dash(s - w + d - a, s - w - d + a)
        self.player.move_coords(s - w + d - a, s - w - d + a, own_speed=True)

    def add_particle(self, x, y):
        self.parts.append(Particle([x, y]))

    def fps_counter(self):
        fps_t = self.font.render(str(int(self.clock.get_fps())), True, 'Blue')
        self.display.blit(fps_t, (0, 0))

    def update(self):
        self.board.update(self.player.pos, 500)

    def render(self):
        nx, ny = self.camera.pos
        nx, ny = back_convert(nx + self.W // 4, ny + self.H // 4)
        self.board.render(self.display, *self.camera.pos, 200, nx, ny)

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
