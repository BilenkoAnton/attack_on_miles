import os
from random import choice, shuffle

import pygame
from pygame.mixer import music

SOUNDTREK_VOLUME = 0.2
NOT_STANDART_SOUNDTREK_VOLUME = {'Instrumental_Fast_Forward.mp3': 1.2}
SOUNDTREK_LIST = list(os.scandir('audio/soundtrek'))
shuffle(SOUNDTREK_LIST)
BELKIN_PHRASES = list(os.scandir('audio/belkin'))
IMPACT_DIRECTORY = 'audio/impact/'


def random_belkin_phrase():
    pygame.mixer.Sound(choice(BELKIN_PHRASES)).play()


def weapon_effect(thing):
    effect_dict = {'spear': 'spear_in_order.mp3', 'rhino': 'rhino.mp3',
                   'electro': 'flash_2.mp3', 'mysterio_laugh': 'Evil_Laugh.mp3',
                   'punch': 'punch.mp3'}
    pygame.mixer.Sound(f'{IMPACT_DIRECTORY}{effect_dict.get(thing)}').play()


def setting_volume(sound_name):
    if NOT_STANDART_SOUNDTREK_VOLUME.get(sound_name):
        music.set_volume(NOT_STANDART_SOUNDTREK_VOLUME.get(sound_name))
    else:
        music.set_volume(SOUNDTREK_VOLUME)


def play_soundtrek():
    if not music.get_busy() and len(SOUNDTREK_LIST) >= 1:
        sound = SOUNDTREK_LIST.pop()
        music.load(sound)
        setting_volume(sound.name)
        music.play()
