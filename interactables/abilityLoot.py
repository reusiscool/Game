from interactables.baseInteractable import BaseInteractable
from utils.infoDisplay import generate_description
from utils.savingConst import SavingConstants
from utils.utils import load_image
from weapons.ability import Ability


class AbilityLoot(BaseInteractable):
    def __init__(self, pos, ability: Ability):
        s = load_image('ability', 'ability_loot.png', color_key='white')
        self.ability = ability
        super().__init__(pos, [s])
        self.hitbox_size = 40

    def get_desc(self):
        return generate_description('large_font', self.ability.stats.to_dict(), 'Ability')

    def interact(self, obj, board):
        board.pop_loot(self)
        obj.ability = self.ability

    def serialize(self):
        return SavingConstants().get_const(AbilityLoot), self.pos, *self.ability.serialize()

    @classmethod
    def read(cls, line):
        pos = eval(line[1])
        type_ = SavingConstants().get_type(int(line[2]))
        return cls(pos, type_.read(line[2:]))
