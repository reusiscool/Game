import pygame

from player import Player
from states import Stat


class UIGame:
    def __init__(self, player: Player, win_size):
        self.win_w, self.win_h = win_size
        self.y = self.win_h * 6 // 7
        self.hp = pygame.Rect(self.win_w // 20, self.y + self.win_h // 35, self.win_w // 5, self.win_h // 30)
        self.mana = pygame.Rect(self.win_w // 20, self.y + self.win_h // 12, self.win_w // 5, self.win_h // 30)
        self.player = player

    def render(self, surf):
        pygame.draw.rect(surf, 'black', pygame.Rect(0, self.y, self.win_w, self.win_h - self.y))
        pygame.draw.rect(surf, 'grey', self.hp)
        pygame.draw.rect(surf, 'grey', self.mana)
        pygame.draw.rect(surf, 'red', pygame.Rect(self.hp.x, self.hp.y,
                                                  self.player.stats[Stat.Health] * self.hp.width / self.player.stats[Stat.MaxHealth],
                                                  self.hp.height))
        pygame.draw.rect(surf, 'blue', pygame.Rect(self.mana.x, self.mana.y,
                                                   self.player.stats[Stat.Mana] * self.mana.width / self.player.stats[Stat.MaxMana],
                                                   self.mana.height))
