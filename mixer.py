import os
import pygame


class Mixer:
    def __init__(self):
        self.pick = pygame.mixer.Sound(os.path.join('sounds', 'pickupCoin.wav'))
        self.fail = pygame.mixer.Sound(os.path.join('sounds', 'fail.wav'))
        self.ability = pygame.mixer.Sound(os.path.join('sounds', 'ability.wav'))
        self.death = pygame.mixer.Sound(os.path.join('sounds', 'kill.wav'))
        self.sounds = [self.pick, self.fail, self.ability, self.death]

    def change_volume(self, volume):
        for sound in self.sounds:
            sound.set_volume(volume)

    def on_pick(self):
        self.pick.play()

    def on_fail(self):
        self.fail.play()

    def on_ability(self):
        self.ability.play()

    def on_death(self):
        self.death.play()


mixer = None


def single_mixer() -> Mixer:
    global mixer
    if mixer is None:
        mixer = Mixer()
    return mixer
