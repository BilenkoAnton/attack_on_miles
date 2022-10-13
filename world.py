import pygame

from characters_and_weapons import Rhino, Miles, Kraven, Electro, Mysterio


class World:
    def __init__(self, normal_bg_color=(0, 0, 255), mysterios_bg_color=(127, 127, 127), screen_parameters=(1200, 600)):
        self.screen = pygame.display.set_mode(screen_parameters)
        self.normal_bg_color = normal_bg_color
        self.mysterios_bg_color = mysterios_bg_color
        self.characters_dict = {'Rhino': Rhino(self.screen), 'Miles': Miles(self.screen),
                           'Kraven': Kraven(self.screen), 'Electro': Electro(self.screen),
                           'Mysterio': Mysterio(self.screen)}
        self.mysterios_characters_dict = {key: self.characters_dict.get(key) for key in self.characters_dict if
                                     key == 'Miles' or key == 'Mysterio'}
        self.actuality_characters_dict = self.characters_dict
        self.actuality_bg_color = self.normal_bg_color
        self.normal_world = True

    def check_mysterio_world(self, actuality_characters_dict):
        if actuality_characters_dict.get('Mysterio').mysterio_world:
            return True
        else:
            return False

    def replace_world(self):
        if self.actuality_bg_color == self.normal_bg_color:
            self.actuality_bg_color = self.mysterios_bg_color
            self.actuality_characters_dict = self.mysterios_characters_dict
        elif self.actuality_bg_color == self.mysterios_bg_color:
            self.actuality_bg_color = self.normal_bg_color
            self.actuality_characters_dict = self.characters_dict

    def main_function(self):
        if self.normal_world == self.check_mysterio_world(self.actuality_characters_dict):
            self.normal_world = not self.check_mysterio_world(self.actuality_characters_dict)
            self.replace_world()
