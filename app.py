import os

import pygame
import sys

from scenes.deathScreen import DeathScreen
from scenes.gameScene import GameScene
from scenes.pauseScene import PauseScene
from scenes.scene import Scene
from scenes.settingScene import SettingScene
from scenes.titleScene import TitleScene
from scenes.winScreen import WinScreen


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
        self.ts = TitleScene(self.screen)
        self.pause = PauseScene(self.screen)
        self.dead = DeathScreen(self.screen)
        self.win = WinScreen(self.screen)
        self.cur_scene = self.ts

    def run(self):
        while True:
            # todo fix pause gamescene reload
            res = self.cur_scene.run()
            if res == Scene.Exit:
                pygame.quit()
                sys.exit()
            if res == Scene.GameScene:
                self.cur_scene = GameScene(self.screen, not self.has_save())
                continue
            if res == Scene.TitleScene:
                self.cur_scene = self.ts
                continue
            if res == Scene.NewGame:
                self.restart()
                self.cur_scene = GameScene(self.screen, True)
                continue
            if res == Scene.Pause:
                self.cur_scene.save()
                self.cur_scene = self.pause
                continue
            if res == Scene.SettingScene:
                self.cur_scene = self.settings
                continue
            if res == Scene.DeathScreen:
                self.cur_scene = self.dead
                continue
            if res == Scene.WinScreen:
                self.cur_scene = self.win

    def has_save(self):
        with open(os.path.join('save_files', 'GameState.txt')) as f:
            k = int(f.read())
        return k != 0

    def restart(self):
        with open(os.path.join('save_files', 'GameState.txt'), 'w') as f:
            f.write('0')
