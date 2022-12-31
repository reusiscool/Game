from dataclasses import dataclass
from enum import Enum
import pygame


class RoomType(Enum):
    Null = 1
    Weapon = 2
    Shop = 3
    DarkShop = 4
    Key = 5
    Puzzle = 6
    Portal = 7
    Player = 8
    Combat = 9


@dataclass(slots=True)
class Room:
    rect: pygame.Rect
    type_: RoomType = RoomType.Null
