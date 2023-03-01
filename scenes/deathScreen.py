import pygame

from mixer import Mixer
from scenes.scene import Scene
from scenes.baseScene import BaseScene


class DeathScreen(BaseScene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.rescale()

    def rescale(self):
        self.W, self.H = self.screen.get_size()
        bw, bh = self.W // 10, self.H // 20
        self.return_btn = pygame.Rect(self.W // 2 - bw, self.H // 2 + 2 * bh, bw * 2, bh * 2)
        self.return_txt = self.scale(self.font.render('Return'), self.return_btn.size)
        self.return_txt.set_colorkey('black')
        self.over_txt = self.font.render('Game Over')
        self.over_txt = self.scale(self.over_txt, (self.W // 2, self.H // 5))

    def render(self):
        self._render_btn(self.return_btn, self.return_txt)
        dx, dy = self.over_txt.get_size()
        self.screen.blit(self.over_txt, ((self.W - dx) // 2, self.H // 2 - dy))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            Mixer().on_click()
            if self.return_btn.collidepoint(*event.pos):
                return Scene.TitleScene
