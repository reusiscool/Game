import pygame
import sys
from scenes.gameScene import GameScene
from scenes.pauseScene import PauseScene
from scenes.scene import Scene
from scenes.settingScene import SettingScene
from scenes.titleScene import TitleScene


class App:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.FPS = 60
        self.screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                               pygame.display.Info().current_h))
        self.settings = SettingScene(self.screen)
        size = self.settings.resolution
        self.display = pygame.Surface((size[0] // 2, size[1] // 2))
        self.clock = pygame.time.Clock()
        self.gs = GameScene(self.screen)
        self.ts = TitleScene(self.screen)
        self.pause = PauseScene(self.screen)
        self.cur_scene = self.ts

    def run(self):
        while True:
            res = self.cur_scene.run()
            if res == Scene.Exit:
                if self.cur_scene != self.ts:
                    self.gs.save()
                pygame.quit()
                sys.exit()
            if res == Scene.GameScene:
                self.cur_scene = self.gs
                continue
            if res == Scene.TitleScene:
                self.cur_scene = self.ts
                self.gs.save()
                continue
            if res == Scene.NewGame:
                self.gs.restart()
                self.cur_scene = self.gs
                continue
            if res == Scene.Pause:
                self.cur_scene = self.pause
                continue
            if res == Scene.SettingScene:
                self.cur_scene = self.settings
