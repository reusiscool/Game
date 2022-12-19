from enum import Enum
import pygame


class Stat(Enum):
    Mana = 1
    Health = 2
    Gold = 3
    MaxHealth = 4
    MaxMana = 5
    Speed = 6
    DashSpeed = 7


def return_pic(state: Stat):
    s = pygame.Surface((10, 10))
    s.fill('blue')
    loot_pics = {Stat.Mana: [s]}
    return loot_pics[state]
