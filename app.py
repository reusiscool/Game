import pygame
import sys
from scenes.gameScene import GameScene
from scenes.scene import Scene
from scenes.titleScene import TitleScene


class App:
    def __init__(self, size=(1600, 900)):
        pygame.init()
        self.FPS = 60
        self.screen = pygame.display.set_mode(size)
        self.display = pygame.Surface((size[0] // 2, size[1] // 2))
        self.clock = pygame.time.Clock()
        self.gs = GameScene(self.screen)
        self.ts = TitleScene(self.screen)
        self.cur_scene = self.ts

    def run(self):
        while True:
            res = self.cur_scene.run()
            if res == Scene.Exit:
                self.gs.save()
                pygame.quit()
                sys.exit()
            if res == Scene.GameScene:
                self.cur_scene = self.gs
                continue
            if res == Scene.TitleScene:
                self.cur_scene = self.ts
