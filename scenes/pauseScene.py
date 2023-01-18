import pygame

from mixer import Mixer
from scenes.scene import Scene
from utils.customFont import single_font


class PauseScene:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = single_font('large_font')
        self.eval_size()

    def eval_size(self):
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

    def scale(self, surf, to_size):
        sx, sy = to_size
        x, y = surf.get_size()
        k = min(sx / x, sy / y) * 0.85
        x *= k
        y *= k
        return pygame.transform.scale(surf, (x, y))

    def render(self):
        self._render_btn(self.quit_button, self.quit_txt)
        self._render_btn(self.setting_button, self.setting_txt)
        self._render_btn(self.continue_button, self.continue_txt)

    def _render_btn(self, btn, txt):
        pygame.draw.rect(self.screen, 'white', btn)
        x = btn.centerx - txt.get_width() // 2
        y = btn.centery - txt.get_height() // 2
        self.screen.blit(txt, (x, y))

    def run(self):
        self.eval_size()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Scene.Exit
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
                self.screen.fill('pink')
                self.render()
                pygame.display.flip()
