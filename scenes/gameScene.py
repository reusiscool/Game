import csv
import os

import pygame

from items.itemConst import ItemConstants
from utils.converters import mum_convert, back_convert
from surroundings.board import Board
from utils.camera import Camera
from inventory import Inventory
from items.healItem import HealItem
from minimap import Minimap
from player import Player, PlayerStats
from uigame import UIGame
from utils.utils import normalize
from scenes.scene import Scene
from weapons.ability import Ability
from weapons.sword import SwordStats, Sword


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
        is_new_session = self._gen_new()
        if is_new_session:
            self.player: Player = self._gen_player()
        else:
            self.player = self._load_player()
        self.board: Board = Board(100, self.player, 700,
                                  self.display.get_width() * 3 // 5, is_new_session)
        self.gameui: UIGame = UIGame(self.player, (self.W // 2, self.H // 2))
        self.minimap: Minimap = Minimap(self.board.reader.map_, self.board.reader.level.rooms)

    def _gen_new(self):
        with open(os.path.join('levels', 'GameState.txt')) as f:
            k = int(f.readline())
        return k == 0

    def _gen_player(self):
        ps = PlayerStats((0, 0, 5), 4, 100, 100, 100, 100, 30, 3)
        invent = Inventory(7, self.display.get_size())
        hl = HealItem(20)
        invent.add_item(hl)
        sw_st1 = SwordStats(25, 45, 40, 40, 30)
        sw_st2 = SwordStats(10, 100, 45, 60, 60)
        return Player(ps, invent, [Sword(sw_st1), Sword(sw_st2)], Ability())

    def _load_player(self):
        with open(os.path.join('levels', 'player.csv')) as f:
            reader = csv.reader(f)
            stat_line = next(reader)
            w1 = next(reader)
            w2 = next(reader)
            abl = next(reader)
            items = []
            for item in reader:
                items.append(item)
        pos = eval(stat_line[0])
        stats = [int(i) for i in stat_line[1:]]
        stats = PlayerStats((*pos, 10), *stats)
        st1 = SwordStats(*(int(i) for i in w1))
        st2 = SwordStats(*(int(i) for i in w2))
        weapons1 = [Sword(st1), Sword(st2)]
        invent = Inventory(7, self.display.get_size())
        for i in items:
            item = ItemConstants().types[int(i[0])]
            item = item(*(int(i) for i in i[1:]))
            invent.add_item(item)
        return Player(stats, invent, weapons1, Ability())

    def check_controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.player.secondary_attack()

        s = keys[pygame.K_s]
        d = keys[pygame.K_d]
        w = keys[pygame.K_w]
        a = keys[pygame.K_a]
        if not a + d + w + s:
            return
        if keys[pygame.K_LSHIFT]:
            self.player.dash(s - w + d - a, s - w - d + a)
        self.player.move_input(s - w + d - a, s - w - d + a)

    def fps_counter(self):
        fps_t = self.font.render(str(int(self.clock.get_fps())), True, 'Blue')
        self.display.blit(fps_t, (0, 0))

    def update(self):
        if self.player.stats.health <= 0:
            self.board.on_death()
        if self.player.is_passing:
            self.player.is_passing = False
            self.board = Board(100, self.player, 700, self.display.get_width() * 3 // 5, True)
            self.minimap: Minimap = Minimap(self.board.reader.map_, self.board.reader.level.rooms)
            return
        x, y = pygame.mouse.get_pos()
        cx, cy = self.camera.pos
        x *= 0.5
        y *= 0.5
        x += cx
        y += cy
        x, y = back_convert(x, y)
        self.player.looking_direction = normalize(x - self.player.x, y - self.player.y)
        self.board.update()
        self.minimap.update(self.board)
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.player.inventory.update(pygame.mouse.get_pos())

    def render(self):
        nx, ny = self.camera.pos
        nx, ny = back_convert(nx + self.W // 4, ny + self.H // 4)
        self.board.render(self.display, *self.camera.pos, nx, ny)
        self.gameui.render(self.display, pygame.mouse.get_pos())
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.player.inventory.render(self.display)
        if pygame.key.get_pressed()[pygame.K_LCTRL]:
            self.minimap.render(self.display)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Scene.Exit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return Scene.TitleScene
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    if pygame.key.get_pressed()[pygame.K_TAB]:
                        self.player.inventory.use_item(pygame.mouse.get_pos(), self.player)
                    else:
                        self.player.attack()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                    if pygame.key.get_pressed()[pygame.K_TAB]:
                        self.player.inventory.discard_item(pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.player.change_weapon()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.player.is_interacting = True
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

    def save(self):
        self.board.save()
