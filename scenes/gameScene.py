from random import randint
import pygame
import csv
import os

from entity import Entity
from mixer import Mixer
from scenes.skillScene import SkillScene
from surroundings.particles import Particle
from surroundings.rooms import RoomType
from utils.converters import mum_convert, back_convert
from surroundings.board import Board
from utils.camera import Camera
from inventory import Inventory
from items.healItem import HealItem
from minimap import Minimap
from player import Player, PlayerStats
from uigame import UIGame
from utils.customFont import single_font
from utils.savingConst import SavingConstants
from utils.utils import normalize
from scenes.scene import Scene
from weapons.ability import Ability, AbilityStats
from weapons.dropSwords import ManaSwordStats, ManaSword
from weapons.sword import SwordStats, Sword


class GameScene:
    def __init__(self, screen: pygame.Surface, gen_new):
        pygame.init()
        self.FPS = 60
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.screen = screen
        self.W, self.H = screen.get_size()
        self.display = pygame.Surface((self.W // 2, self.H // 2))
        self.clock = pygame.time.Clock()
        self.camera = Camera([0, 0])
        self.particles = []
        self.player = self._gen_player() if gen_new else self._load_player()
        self.skill_scene = SkillScene(self.screen, self.player)
        if not gen_new:
            self.skill_scene.read()
            self.player.skills = self.skill_scene.get_skills(True)
        self.board: Board = Board(100, self.player, 700,
                                  self.display.get_width() * 3 // 5, gen_new)
        self.gameui: UIGame = UIGame(self.player, (self.W // 2, self.H // 2))
        self.minimap: Minimap = Minimap(self.board, read=not gen_new)
        x, y = self.player.pos
        x1, y1 = mum_convert(x, y)
        self.camera.snap((x1, y1), self.display.get_size())
        self.death_time = 0
        self.won = False

    def on_rescale(self):
        self.W, self.H = self.screen.get_size()
        self.display = pygame.Surface((self.W // 2, self.H // 2))
        self.board.render_distance = self.display.get_width() * 3 // 5
        self.gameui: UIGame = UIGame(self.player, (self.W // 2, self.H // 2))
        self.player.inventory.resize(self.display.get_size())

    def _gen_player(self):
        ps = PlayerStats((0, 0, 5), 4, 100, 100, 100, 100, 30, 3, 0, 1)
        invent = Inventory(7, self.display.get_size())
        hl = HealItem(20)
        invent.add_item(hl)
        sw_st1 = ManaSwordStats(25, 45, 40, 40, 30, 0, 10)
        sw_st2 = SwordStats(10, 100, 45, 60, 60, 0)
        ast = AbilityStats(20, 20, 10)
        return Player(ps, invent, [ManaSword(sw_st1), Sword(sw_st2)], Ability(ast))

    def _load_player(self):
        with open(os.path.join('save_files', 'player.csv')) as f:
            reader = csv.reader(f)
            inv_size = next(reader)[0]
            stat_line = next(reader)
            w1 = next(reader)
            w2 = next(reader)
            ast = next(reader)
            items = []
            for item in reader:
                items.append(item)
        abl = SavingConstants().load(ast)
        pos = eval(stat_line[0])
        stats = [int(i) if i.isdigit() else float(i) for i in stat_line[1:]]
        stats = PlayerStats((*pos, 10), *stats)
        weapons1 = [SavingConstants().load(w1), SavingConstants().load(w2)]
        invent = Inventory(int(inv_size), self.display.get_size())
        for i in items:
            item = SavingConstants().get_type(int(i[0]))
            item = item(*(int(i) for i in i[1:]))
            invent.add_item(item)
        return Player(stats, invent, weapons1, abl)

    def check_controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.player.secondary_attack()
        if pygame.mouse.get_pressed(3)[2]:
            self.player.is_blocking = True

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

    def restart(self):
        with open(os.path.join('save_files', 'GameState.txt'), 'w') as f:
            f.write('0')
        self.death_time = 0
        self.won = False
        self.player = self._gen_player()
        self.gameui: UIGame = UIGame(self.player, (self.W // 2, self.H // 2))
        self.board = Board(100, self.player, 700, self.display.get_width() * 3 // 5, True)
        self.minimap: Minimap = Minimap(self.board)
        x, y = self.player.pos
        x1, y1 = mum_convert(x, y)
        self.camera.snap((x1, y1), self.display.get_size())

    def update(self):
        if self.player.stats.health <= 0 and not self.death_time:
            self.death_time = 20
        if self.player.is_passing:
            if self.board.reader.level.level_number == 10:
                self.won = True
                return
            self.player.is_passing = False
            self.board = Board(100, self.player, 700, self.display.get_width() * 3 // 5, True)
            self.minimap: Minimap = Minimap(self.board)
            x, y = self.player.pos
            x1, y1 = mum_convert(x, y)
            self.camera.snap((x1, y1), self.display.get_size())
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
        for ent in self.board.get_entities(self.player.pos, self.board.update_distance):
            if isinstance(ent, Entity) and ent.damage_time == 1:
                for _ in range(5):
                    self.particles.append(Particle(ent.pos, 5))

    def render(self):
        nx, ny = self.camera.pos
        nx, ny = back_convert(nx + self.W // 4, ny + self.H // 4)
        self.board.render(self.display, *self.camera.pos, nx, ny)
        self.gameui.render(self.display, pygame.mouse.get_pos())
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.player.inventory.render(self.display)
        if pygame.key.get_pressed()[pygame.K_LCTRL]:
            self.minimap.render(self.display)
        for i in range(len(self.particles) - 1, -1, -1):
            if not self.particles[i].render(self.display, *self.camera.pos):
                self.particles.pop(i)

    def on_click(self, event):
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.player.inventory.use_item(pygame.mouse.get_pos(), self.player)
            return
        if self.gameui.on_click(event.pos):
            self.skill_scene.run()
            self.player.skills = self.skill_scene.get_skills(True)
            return
        self.player.attack()

    def run(self):
        self.on_rescale()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Scene.Exit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return Scene.Pause
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    self.on_click(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                    if pygame.key.get_pressed()[pygame.K_TAB]:
                        self.player.inventory.discard_item(pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.player.change_weapon()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.player.is_interacting = True
            if self.death_time:
                if self.death_time == 1:
                    if not randint(0, 20):
                        self.fake_death()
                        continue
                    self.board.on_death()
                    return Scene.DeathScreen
                self.death_time -= 1
            if self.won:
                self.board.on_death()
                return Scene.WinScreen
            x, y = self.player.pos
            x1, y1 = mum_convert(x, y)
            self.camera.adjust((x1, y1), self.display.get_size())
            self.update()
            self.display.fill((250, 80, 100))
            self.check_controls()
            self.render()
            # self.fps_counter()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(self.FPS)

    def fake_death(self):
        black_time = 60
        first_sign_time = 150
        second_sign_time = 100
        fade_time = 200
        self.death_time = 0
        self.player.stats.health = self.player.stats.max_health
        self.board.dead = False
        self.board.add_entity(self.player)
        font = single_font('large_font')
        first_sign_txt = self.scale(font.render('There are fates worse than death.'), (self.W // 2, self.H // 2))
        first_sign_txt.set_colorkey('black')

        second_sign_txt = self.scale(font.render('Get up.'), (self.W // 2, self.H // 2))
        second_sign_txt.set_colorkey('black')

        mixer = Mixer()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Scene.Exit
            self.screen.fill('black')
            if black_time:
                black_time -= 1
                if black_time == 1:
                    mixer.on_cassette()
            elif first_sign_time:
                self.blit_centre(self.screen, first_sign_txt)
                first_sign_time -= 1
                if first_sign_time == 1:
                    mixer.on_cassette()
            elif second_sign_time:
                self.blit_centre(self.screen, second_sign_txt)
                second_sign_time -= 1
                if second_sign_time == 20:
                    mixer.on_reanimate()
            elif fade_time:
                self.blit_centre(self.screen, second_sign_txt)
                s = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
                s.fill((255, 255, 255, 225 * (200 - fade_time) // 200))
                self.screen.blit(s, (0, 0))
                fade_time -= 1
            else:
                mixer.on_reanimate_end()
                return
            pygame.display.update()
            self.clock.tick(60)

    def blit_centre(self, blit_surf, surf):
        w, h = blit_surf.get_size()
        sw, sh = surf.get_size()
        blit_surf.blit(surf, ((w - sw) // 2, (h - sh) // 2))

    def scale(self, surf, to_size):
        sx, sy = to_size
        x, y = surf.get_size()
        k = min(sx / x, sy / y) * 0.85
        x *= k
        y *= k
        return pygame.transform.scale(surf, (x, y))

    def save(self):
        self.board.save()
        self.skill_scene.save()
        self.minimap.save()
