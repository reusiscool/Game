import pygame

from interactables.baseInteractable import BaseInteractable
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants
from weapons.ability import Ability


class AbilityLoot(BaseInteractable):
    def __init__(self, pos, ability: Ability):
        s = pygame.Surface((20, 20))
        s.fill('cyan')
        image_list = [s]
        self.ability = ability
        super().__init__(pos, image_list)
        self.hitbox_size = 40

    def get_desc(self):
        return generate_description('large_font', self.ability.stats.to_dict(), 'Ability')

    def interact(self, obj, board):
        board.pop_loot(self)
        obj.ability = self.ability

    def serialize(self):
        return SavingConstants().get_const(AbilityLoot), self.pos, *self.ability.serialize()
