from random import randint, choice
import pygame

from converters import mum_convert, back_convert
from board import Board
from camera import Camera
from enemy import Enemy
from player import Player
from particles import Particle
from uigame import UIGame
from utils import load_image, normalize
from scene import Scene


class GameScene:
    def __init__(self, screen: pygame.Surface):
        pygame.init()
        self.FPS = 60
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.screen = screen
        self.W, self.H = screen.get_size()
        self.display = pygame.Surface((self.W // 2, self.H // 2))
        self.clock = pygame.time.Clock()
        self.camera = Camera([0, 0])
        ls = []
        for i in range(17):
            for j in range(7):
                ls.append(load_image('player', f'player{i}.png', color_key='white'))
        self.player = Player((0, 0), 15, ls, 4)
        self.parts: list[Particle] = []
        self.board = Board(100, self.player)
        self.board.add_entity(self.player)
        self.gameui = UIGame(self.player, (self.W // 2, self.H // 2))
        for i in range(10):
            self.board.add_entity(Enemy((500 + i * 15, 500), 5, [load_image('grass.jpg')], 2, health=100))

    def check_controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.player.secondary_attack()

        s = keys[pygame.K_s]
        d = keys[pygame.K_d]
        w = keys[pygame.K_w]
        a = keys[pygame.K_a]
        if not (a + d + w + s):
            return
        if keys[pygame.K_LSHIFT]:
            self.player.dash(s - w + d - a, s - w - d + a)
        self.player.move_input(s - w + d - a, s - w - d + a)

    def add_particle(self, pos):
        self.parts.append(Particle(pos, choice((randint(3, 4), 0, 0))))

    def fps_counter(self):
        fps_t = self.font.render(str(int(self.clock.get_fps())), True, 'Blue')
        self.display.blit(fps_t, (0, 0))

    def update(self):
        self.board.update(self.player.pos, 500)
        # for i in self.board.get_entities(self.player.pos, 500):
        #     if i.collided:
        #         self.add_particle(i.pos)
        x, y = pygame.mouse.get_pos()
        cx, cy = self.camera.pos
        x *= 0.5
        y *= 0.5
        x += cx
        y += cy
        x, y = back_convert(x, y)
        self.player.looking_direction = normalize(x - self.player.x, y - self.player.y)

    def render(self):
        nx, ny = self.camera.pos
        nx, ny = back_convert(nx + self.W // 4, ny + self.H // 4)
        self.board.render(self.display, *self.camera.pos, 450, nx, ny)
        for i in range(len(self.parts) - 1, -1, -1):
            if not self.parts[i].render(self.display, *self.camera.pos):
                self.parts.pop(i)
        self.gameui.render(self.display)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Scene.Exit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return Scene.TitleScene
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    self.player.attack()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    self.player.change_weapon()
            x, y = self.player.pos
            x1, y1 = mum_convert(x, y)
            self.camera.adjust((x1, y1), self.display.get_size())
            self.update()
            self.display.fill((250, 80, 100))
            self.check_controls()
            self.render()
            self.fps_counter()
            pygame.draw.circle(self.display, 'yellow', (self.W // 4, self.H // 4), 3)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(self.FPS)
