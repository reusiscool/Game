import pygame

from mixer import Mixer
from scenes.scene import Scene
from utils.customFont import single_font


class DeathScreen:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = single_font('large_font')
        self.resize()

    def resize(self):
        self.W, self.H = self.screen.get_size()
        bw, bh = self.W // 10, self.H // 20
        self.return_btn = pygame.Rect(self.W // 2 - bw, self.H // 2 + 2 * bh, bw * 2, bh * 2)
        self.return_txt = self.scale(self.font.render('Return'), self.return_btn.size)
        self.return_txt.set_colorkey('black')
        self.over_txt = self.font.render('Game Over')
        self.over_txt = self.scale(self.over_txt, (self.W // 2, self.H // 5))

    def scale(self, surf, to_size):
        sx, sy = to_size
        x, y = surf.get_size()
        k = min(sx / x, sy / y) * 0.85
        x *= k
        y *= k
        return pygame.transform.scale(surf, (x, y))

    def _render_btn(self, btn, txt, color='white'):
        pygame.draw.rect(self.screen, color, btn)
        x = btn.centerx - txt.get_width() // 2
        y = btn.centery - txt.get_height() // 2
        self.screen.blit(txt, (x, y))

    def render(self):
        self._render_btn(self.return_btn, self.return_txt)
        dx, dy = self.over_txt.get_size()
        self.screen.blit(self.over_txt, ((self.W - dx) // 2, self.H // 2 - dy))

    def run(self):
        self.resize()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Scene.Exit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    Mixer().on_click()
                    if self.return_btn.collidepoint(*event.pos):
                        return Scene.TitleScene
            self.screen.fill('black')
            self.render()
            pygame.display.flip()
