import os
import pygame

from utils.singleton import Singleton


class Mixer(metaclass=Singleton):
    def __init__(self):
        self.pick = pygame.mixer.Sound(os.path.join('sounds', 'pickupCoin.wav'))
        self.fail = pygame.mixer.Sound(os.path.join('sounds', 'fail.wav'))
        self.ability = pygame.mixer.Sound(os.path.join('sounds', 'ability.wav'))
        self.death = pygame.mixer.Sound(os.path.join('sounds', 'kill.wav'))
        self.ear = pygame.mixer.Sound(os.path.join('sounds', 'earRing.wav'))
        self.cassette = pygame.mixer.Sound(os.path.join('sounds', 'cassette.wav'))
        self.click = pygame.mixer.Sound(os.path.join('sounds', 'click.wav'))
        pygame.mixer.music.load(os.path.join('sounds', 'music.wav'))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        self.sounds = [self.pick, self.fail, self.ability, self.death,
                       self.ear, self.cassette, self.click]

    def change_volume(self, volume):
        for sound in self.sounds:
            sound.set_volume(volume)

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def on_pick(self):
        self.pick.play()

    def on_fail(self):
        self.fail.play()

    def on_ability(self):
        self.ability.play()

    def on_death(self):
        self.death.play()

    def on_reanimate(self):
        self.ear.play(maxtime=5000)

    def on_reanimate_end(self):
        self.ear.stop()

    def on_cassette(self):
        self.cassette.play(maxtime=2000)

    def on_click(self):
        self.click.play()
