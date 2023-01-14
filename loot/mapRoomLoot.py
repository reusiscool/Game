import pygame

from loot.baseLoot import BaseLoot
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants


class MapRoomLoot(BaseLoot):
    def __init__(self, pos, room_type):
        self.room_type = room_type
        s = pygame.Surface((10, 10))
        s.fill('green')
        super().__init__(pos, [s])

    @property
    def desc(self):
        return generate_description('large_font', ['Allows you to read',
                                                   f'{self.room_type} rooms on map'], "Map read item")

    def add_amount(self, obj, board):
        if self.room_type not in obj.stats.revealed_rooms:
            obj.stats.revealed_rooms.append(self.room_type)

    def serialize(self):
        return SavingConstants().get_const(MapRoomLoot), self.pos, self.room_type.value
