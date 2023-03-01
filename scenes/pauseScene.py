import pygame

from mixer import Mixer
from scenes.scene import Scene
from scenes.baseScene import BaseScene


class PauseScene(BaseScene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.rescale()

    def rescale(self):
        self.W, self.H = self.screen.get_size()
        bw, bh = self.W // 10, self.H // 20
        self.continue_button = pygame.Rect(self.W // 2 - bw, self.H // 2 - 4 * bh, bw * 2, bh * 2)
        self.setting_button = pygame.Rect(self.W // 2 - bw, self.H // 2 - bh, bw * 2, bh * 2)
        self.quit_button = pygame.Rect(self.W // 2 - bw, self.H // 2 + 2 * bh, bw * 2, bh * 2)
        self.continue_txt = self.scale(self.font.render('Continue'), self.continue_button.size)
        self.continue_txt.set_colorkey('black')
        self.quit_txt = self.scale(self.font.render('Main Menu'), self.quit_button.size)
        self.quit_txt.set_colorkey('black')
        self.setting_txt = self.scale(self.font.render('Settings'), self.setting_button.size)
        self.setting_txt.set_colorkey('black')

    def render(self):
        self._render_btn(self.quit_button, self.quit_txt)
        self._render_btn(self.setting_button, self.setting_txt)
        self._render_btn(self.continue_button, self.continue_txt)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return Scene.GameScene
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            Mixer().on_click()
            if self.continue_button.collidepoint(*event.pos):
                return Scene.GameScene
            if self.quit_button.collidepoint(*event.pos):
                return Scene.TitleScene
            if self.setting_button.collidepoint(*event.pos):
                return Scene.SettingScene

    @property
    def bg_color(self):
        return 'pink'
