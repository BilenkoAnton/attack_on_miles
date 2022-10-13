import pygame

from audio import play_soundtrek
from controls import events
from world import World


def prepare_game():
    pygame.init()
    pygame.display.set_caption('Attack on Miles')


def main_cycle():
    world = World()
    while True:
        world.main_function()
        events(world.characters_dict.get('Miles'))
        world.screen.fill(world.actuality_bg_color)
        for character in world.actuality_characters_dict.values():
            character.do_main_functions()
            character.damage_opponent(world.characters_dict.get('Miles'))
            if character.auto_mod:
                character.auto_control(world.characters_dict.get('Miles'))
        play_soundtrek()
        pygame.display.flip()


def run_game():
    prepare_game()
    main_cycle()
