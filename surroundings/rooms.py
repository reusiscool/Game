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
    id_: int
    type_: RoomType = RoomType.Null

    def pos_to_tiles(self, tile_size):
        return self.rect.center[0] * tile_size, self.rect.center[1] * tile_size
