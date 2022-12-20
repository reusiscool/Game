import pygame

from player import Player
from states import Stat


class UIGame:
    def __init__(self, player: Player, win_size):
        self.win_w, self.win_h = win_size
        self.y = self.win_h * 6 // 7
        self.bg = pygame.Rect(0, self.y, self.win_w, self.win_h - self.y)
        self.gap = self.win_h // 40 >> 1 << 1
        bar_height = self.win_h // 30
        bar_width = self.win_w // 5
        self.hp = pygame.Rect(self.gap, self.y + self.gap, bar_width, bar_height)
        self.mana = pygame.Rect(self.gap, self.y + 2 * self.gap + bar_height, bar_width, bar_height)
        self.player = player
        a = self.win_h - 2 * self.gap - self.y
        self.slot1 = pygame.Rect(self.win_w // 2, self.y + self.gap, a, a)
        self.slot2 = pygame.Rect(self.slot1.right + 2 * self.gap, self.y + self.gap, a, a)

    def render(self, surf):
        pygame.draw.rect(surf, 'black', self.bg)
        pygame.draw.rect(surf, 'grey', self.hp)
        pygame.draw.rect(surf, 'grey', self.mana)
        pygame.draw.rect(surf, 'red', pygame.Rect(self.hp.x, self.hp.y,
                                                  self.player.stats[Stat.Health] * self.hp.width / self.player.stats[Stat.MaxHealth],
                                                  self.hp.height))
        pygame.draw.rect(surf, 'blue', pygame.Rect(self.mana.x, self.mana.y,
                                                   self.player.stats[Stat.Mana] * self.mana.width / self.player.stats[Stat.MaxMana],
                                                   self.mana.height))
        if self.player.weapon_index:
            r = pygame.Rect(self.slot2.x - self.gap // 2, self.slot2.y - self.gap // 2,
                            self.slot2.width + self.gap, self.slot2.height + self.gap)
        else:
            r = pygame.Rect(self.slot1.x - self.gap // 2, self.slot1.y - self.gap // 2,
                            self.slot1.width + self.gap, self.slot1.height + self.gap)
        pygame.draw.rect(surf, 'white', r)
        pygame.draw.rect(surf, 'grey', self.slot1)
        pygame.draw.rect(surf, 'grey', self.slot2)
