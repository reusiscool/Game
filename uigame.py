import os
import pygame

from utils.customFont import single_font
from player import Player
from utils.infoDisplay import generate_description


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

    def _get_level(self):
        with open(os.path.join('save_files', 'GameState.txt')) as f:
            level = int(f.readline())
        return level

    def _render_hp(self, surf):
        pygame.draw.rect(surf, 'grey', self.hp)
        r = pygame.Rect(self.hp.x, self.hp.y,
                        self.player.stats.health * self.hp.width / self.player.stats.max_health,
                        self.hp.height)
        pygame.draw.rect(surf, 'red', r)

    def _render_mana(self, surf):
        pygame.draw.rect(surf, 'grey', self.mana)
        r = pygame.Rect(self.mana.x, self.mana.y,
                        self.player.stats.mana * self.mana.width / self.player.stats.max_mana,
                        self.mana.height)
        pygame.draw.rect(surf, 'blue', r)

    def _render_weapons(self, surf):
        if self.player.weapon_index:
            r = pygame.Rect(self.slot2.x - self.gap // 2, self.slot2.y - self.gap // 2,
                            self.slot2.width + self.gap, self.slot2.height + self.gap)
        else:
            r = pygame.Rect(self.slot1.x - self.gap // 2, self.slot1.y - self.gap // 2,
                            self.slot1.width + self.gap, self.slot1.height + self.gap)
        pygame.draw.rect(surf, 'white', r)
        pygame.draw.rect(surf, 'grey', self.slot1)
        pygame.draw.rect(surf, 'grey', self.slot2)

    def _display_info(self, surf, mouse_pos):
        mx, my = mouse_pos
        mx //= 2
        my //= 2

        if self.slot1.collidepoint(mx, my):
            s = generate_description('large_font', self.player.weapon_list[0].stats.__dict__, 'Weapon')
            surf.blit(s, (surf.get_width() - s.get_width(), 0))
        elif self.slot2.collidepoint(mx, my):
            s = generate_description('large_font', self.player.weapon_list[1].stats.__dict__, 'Weapon')
            surf.blit(s, (surf.get_width() - s.get_width(), 0))
        elif self.hp.collidepoint(mx, my):
            s = generate_description('large_font', [f"{self.player.stats.health} :"
                                                    f" {self.player.stats.max_health}"], "Health")
            surf.blit(s, (surf.get_width() - s.get_width(), 0))
        elif self.mana.collidepoint(mx, my):
            s = generate_description('large_font', [f"{self.player.stats.mana} :"
                                                    f" {self.player.stats.max_mana}"], "Mana")
            surf.blit(s, (surf.get_width() - s.get_width(), 0))

    def render(self, surf: pygame.Surface, mouse_pos):
        pygame.draw.rect(surf, 'black', self.bg)
        self._render_hp(surf)
        self._render_mana(surf)
        self._render_weapons(surf)
        self._display_info(surf, mouse_pos)

        font = single_font('large_font')
        srf = font.render(f'Level - {self._get_level()}')
        surf.blit(srf, (surf.get_width() - srf.get_width() - 5, self.y + 5))

        font = single_font('large_font')
        srf = font.render(f'Gold - {self.player.stats.gold}')
        surf.blit(srf, (surf.get_width() - srf.get_width() - 5, self.y + font.height + 10))
