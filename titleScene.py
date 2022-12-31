import pygame

from scene import Scene


class TitleScene:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.W, self.H = screen.get_size()
        bw, bh = self.W // 20, self.H // 20
        self.start_button = pygame.Rect(self.W // 2 - bw, self.H // 2 - bh, bw * 2, bh * 2)
        self.quit_button = pygame.Rect(self.W // 2 - bw, self.H // 2 + 2 * bh, bw * 2, bh * 2)

    def render(self):
        pygame.draw.rect(self.screen, 'green', self.start_button)
        pygame.draw.rect(self.screen, 'red', self.quit_button)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if self.start_button.collidepoint(*event.pos):
                    return Scene.GameScene
                elif self.quit_button.collidepoint(*event.pos):
                    return Scene.Exit
            self.screen.fill('black')
            self.render()
            pygame.display.flip()
