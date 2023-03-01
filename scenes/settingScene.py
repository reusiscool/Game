import pygame
import csv
import os

from scenes.scene import Scene
from mixer import Mixer
from scenes.baseScene import BaseScene


class SettingScene(BaseScene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.dropped = False
        self.is_fullscreen = False
        self.possible_res = [(1920, 1080), (1600, 900), (1440, 1080), (1280, 960), (1024, 768), (800, 600), (960, 720)]
        self.volume = 0
        self.music_volume = 0
        self.resolution = (0, 0)
        self._read()
        self.drop_buttons = []
        self.drop_buttons_txt = []
        self.rescale()
        self.resize_screen()
        Mixer().change_volume(self.volume)
        Mixer().set_music_volume(self.music_volume)

    def resize_screen(self):
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)

    def rescale(self):
        self.W, self.H = self.screen.get_size()
        bw, bh = self.W // 10, self.H // 20
        sw, sh = self.W // 16, self.H // 50
        self.check_box = pygame.Rect(self.W // 2 - bw, self.H // 2 - 7 * bh, bw * 2, bh * 2)
        self.slider = pygame.Rect(self.W // 2 - sw, self.H // 2 - sh, sw + bw, 2 * sh)
        self.music_slider = pygame.Rect(self.W // 2 - sw, self.H // 2 + 2 * bh, sw + bw, 2 * sh)
        self.dropdown = pygame.Rect(self.W // 2 - bw, self.H // 2 - 4 * bh, bw * 2, bh * 2)
        self.return_btn = pygame.Rect(self.W // 2 - bw, self.H // 2 + 5 * bh, bw * 2, bh * 2)
        self.return_txt = self.scale(self.font.render('Return'), self.return_btn.size)
        self.return_txt.set_colorkey('black')
        self.volume_txt = self.scale(self.font.render('Volume'), self.return_btn.size)
        self.volume_txt.set_colorkey('black')
        self.music_volume_txt = self.scale(self.font.render('Music'), self.return_btn.size)
        self.music_volume_txt.set_colorkey('black')
        self.dropdown_txt = self.scale(self.font.render(f'{self.resolution[0]}:{self.resolution[1]}'),
                                       self.dropdown.size)
        self.dropdown_txt.set_colorkey('black')
        self.check_txt = self.scale(self.font.render('FullScreen'), self.check_box.size)
        self.check_txt.set_colorkey('black')
        self._gen_drop()

    def _gen_drop(self):
        self.drop_buttons_txt.clear()
        self.drop_buttons.clear()
        bw, bh = self.W // 10, self.H // 30
        y0 = self.dropdown.bottom
        for i in range(len(self.possible_res)):
            self.drop_buttons.append(pygame.Rect(self.W // 2 - bw, y0 + i * bh * 2, bw * 2, bh * 2))
            txt = self.scale(self.font.render(f'{self.possible_res[i][0]}:{self.possible_res[i][1]}'),
                             self.dropdown.size)
            txt.set_colorkey('black')
            self.drop_buttons_txt.append(txt)

    def _read(self):
        with open(os.path.join('save_files', 'settings.csv')) as f:
            reader = csv.reader(f)
            self.volume = float(next(reader)[0])
            self.resolution = eval(next(reader)[0])
            self.is_fullscreen = bool(int(next(reader)[0]))
            self.music_volume = float(next(reader)[0])

    def render(self):
        self._render_btn(self.return_btn, self.return_txt)
        self._render_slider(self.slider, self.volume_txt, self.volume)
        self._render_slider(self.music_slider, self.music_volume_txt, self.music_volume)
        self._render_dropdown()
        if self.is_fullscreen:
            self._render_btn(self.check_box, self.check_txt, 'green')
        else:
            self._render_btn(self.check_box, self.check_txt, 'grey')

    def _render_dropdown(self):
        if self.dropped:
            for ind, btn in enumerate(self.drop_buttons):
                if ind % 2:
                    self._render_btn(btn, self.drop_buttons_txt[ind], 'black')
                else:
                    self._render_btn(btn, self.drop_buttons_txt[ind], 'grey')
        self._render_btn(self.dropdown, self.dropdown_txt)

    def _render_slider(self, slide, txt, volume):
        pygame.draw.rect(self.screen, 'grey', slide)
        r = pygame.Rect(0, 0, *txt.get_size())
        r.right = slide.left - 5
        r.centery = slide.centery
        self.screen.blit(txt, r)
        w = slide.w * volume
        r = pygame.Rect(slide.x, slide.y, w, slide.h)
        pygame.draw.rect(self.screen, 'green', r)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.save()
            Mixer().change_volume(self.volume)
            Mixer().set_music_volume(self.music_volume)
            self.resize_screen()
            return Scene.Pause
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            Mixer().on_click()
            if self.dropped:
                self.dropped = False
                for i, btn in enumerate(self.drop_buttons):
                    if btn.collidepoint(*event.pos):
                        self.resolution = self.possible_res[i]
                        self.dropdown_txt = self.scale(self.font.render(f'{self.resolution[0]}:{self.resolution[1]}'),
                                                       self.dropdown.size)
                        self.dropdown_txt.set_colorkey('black')
                        break
                return
            if self.return_btn.collidepoint(*event.pos):
                self.save()
                Mixer().change_volume(self.volume)
                Mixer().set_music_volume(self.music_volume)
                self.resize_screen()
                return Scene.Pause
            if self.slider.collidepoint(*event.pos):
                x, y = event.pos
                dx = x - self.slider.x
                self.volume = dx / self.slider.w
                return
            if self.music_slider.collidepoint(*event.pos):
                x, y = event.pos
                dx = x - self.music_slider.x
                self.music_volume = dx / self.music_slider.w
                return
            if self.dropdown.collidepoint(*event.pos):
                self.dropped = True
                return
            if self.check_box.collidepoint(*event.pos):
                self.is_fullscreen = not self.is_fullscreen

    @property
    def bg_color(self):
        return 'pink'

    def save(self):
        with open(os.path.join('save_files', 'settings.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow((self.volume,))
            writer.writerow((self.resolution,))
            writer.writerow((int(self.is_fullscreen),))
            writer.writerow((self.music_volume,))
