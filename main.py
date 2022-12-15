import sys
import pygame

from converters import mum_convert, back_convert
from board import Board
from camera import Camera
from enemy import Enemy
from player import Player
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
        ls = []
        for i in range(17):
            for j in range(7):
                ls.append(load_image('player', f'player{i+1}.png', color_key='white'))
        self.player = Player((0, 0), 15, ls, 4, 100)
        self.parts: list[Particle] = []
        self.board = Board(100, self.player)
        self.board.add_entity(self.player)
        self.board.add_entity(Enemy((500, 500), 5, [load_image('grass.jpg')], 2, health=100))

    def check_controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.player.attack()

        s = keys[pygame.K_s]
        d = keys[pygame.K_d]
        w = keys[pygame.K_w]
        a = keys[pygame.K_a]
        if not (a + d + w + s):
            return
        if keys[pygame.K_LSHIFT]:
            self.player.dash(s - w + d - a, s - w - d + a)
        self.player.move_input(s - w + d - a, s - w - d + a)

    def add_particle(self, x, y):
        self.parts.append(Particle((x, y)))

    def fps_counter(self):
        fps_t = self.font.render(str(int(self.clock.get_fps())), True, 'Blue')
        self.display.blit(fps_t, (0, 0))

    def update(self):
        self.board.update(self.player.pos, 500)

    def render(self):
        nx, ny = self.camera.pos
        nx, ny = back_convert(nx + self.W // 4, ny + self.H // 4)
        self.board.render(self.display, *self.camera.pos, 450, nx, ny)
        for i in range(len(self.parts) - 1, -1, -1):
            if not self.parts[i].render(self.display, *self.camera.pos):
                self.parts.pop(i)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     x, y = event.pos
                #     cx, cy = self.camera.pos
                #     x *= 0.5
                #     y *= 0.5
                #     x += cx
                #     y += cy
                #     x, y = back_convert(x, y)
                #     r = 10
                #     s = pygame.Surface((2 * r, 2 * r))
                #     pygame.draw.circle(s, 'red', (r, r), r)
                #     self.board.add(Obs((x, y), 2 * r, s))
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
    app = App((800, 600))
    app.run()
