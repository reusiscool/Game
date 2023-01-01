import pygame
from abc import ABC, abstractmethod


class BaseItem(ABC):
    def __init__(self, icon: pygame.Surface, description: pygame.Surface):
        self.description = description
        self.icon = icon

    @abstractmethod
    def use(self, owner) -> bool:
        """:returns bool: whether the item depletes after usage"""
        pass
