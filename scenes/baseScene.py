from abc import abstractmethod, ABC
import pygame

from scenes.scene import Scene
from utils.customFont import single_font


class BaseScene(ABC):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.W, self.H = self.screen.get_size()
        self.font = single_font('large_font')

    @abstractmethod
    def rescale(self):
        pass

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

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @property
    def bg_color(self):
        return 'black'

    def run(self):
        self.rescale()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Scene.Exit
                k = self.handle_event(event)
                if k is not None:
                    return k
            self.screen.fill(self.bg_color)
            self.render()
            pygame.display.flip()
