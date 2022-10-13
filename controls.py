import sys

import pygame

move_control = {pygame.K_RIGHT: {'direction': 'move', 'character': 'any', 'attitude': 'right'},
                pygame.K_LEFT: {'direction': 'move', 'character': 'any', 'attitude': 'left'},
                pygame.K_DOWN: {'direction': 'move', 'character': 'any', 'attitude': 'down'},
                pygame.K_UP: {'direction': 'move', 'character': 'any', 'attitude': 'up'}}

special_control = {pygame.K_SPACE: {'attitude': 'special_1'}}


def events(character=None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if character:
            if event.type == pygame.KEYDOWN and event.key in move_control:
                character.move_value.update({move_control.get(event.key).get('attitude'): True})
                character.turn_around()
            elif event.type == pygame.KEYUP and event.key in move_control:
                character.move_value.update({move_control.get(event.key).get('attitude'): False})
            if event.type == pygame.KEYDOWN and event.key in special_control:
                character.special_maneuver()
