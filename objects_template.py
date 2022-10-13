import datetime

import pygame


class Vision:
    def __init__(self, screen, image_adress):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image_adress = image_adress
        self.image = pygame.image.load(self.image_adress)
        self.left_image = None
        self.rect = self.image.get_rect()

    def output(self):
        self.screen.blit(self.image, self.rect)


class Movable(Vision):
    def __init__(self, screen, image_adress):
        super().__init__(screen=screen, image_adress=image_adress)
        self.move_value = {'left': False, 'right': False, 'up': False, 'down': False}
        self.speed = 1
        self.actual_attitude = 'right'
        self.stoppable = False

    def move(self):
        if not self.stoppable:
            if self.move_value.get('left') and self.rect.left > self.screen_rect.left:
                self.rect.centerx -= self.speed
            if self.move_value.get('right') and self.rect.right < self.screen_rect.right:
                self.rect.centerx += self.speed
            if self.move_value.get('up') and self.rect.top > self.screen_rect.top:
                self.rect.centery -= self.speed
            if self.move_value.get('down') and self.rect.bottom < self.screen_rect.bottom:
                self.rect.centery += self.speed
            self.turn_around()

    def turn_around(self, mustable_turn = False):
        if self.left_image:
            if self.move_value.get('left') or all((mustable_turn, self.actual_attitude == 'right')):
                self.image = pygame.image.load(self.left_image)
                self.actual_attitude = 'left'
            elif self.move_value.get('right') or all((mustable_turn, self.actual_attitude == 'left')):
                self.image = pygame.image.load(self.image_adress)
                self.actual_attitude = 'right'


class GameParticipant:
    def __init__(self):
        self.damage = 10
        self.date_of_create = datetime.datetime.now()

    def damage_opponent(self, opponent):
        pass


class Weapon(GameParticipant, Vision):
    def __init__(self, owner, screen, image_adress):
        super().__init__()
        Vision.__init__(self, screen, image_adress)
        self.owner = owner
        self.used = False

    def damage_opponent(self, opponent):
        if self.rect.colliderect(opponent):
            opponent.live -= self.damage
            self.used = True


class Character(GameParticipant):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.weapon_list = set()
        self.weapons_time = 4
        self.live = 100
        self.auto_mod = True

    def delete_weapons(self, deleting_weapons: list):
        for weapon in deleting_weapons:
            self.weapon_list.remove(weapon)

    def work_with_weapons(self):
        deleting_weapons = []
        for weapon in self.weapon_list:
            if datetime.datetime.now() - weapon.date_of_create > datetime.timedelta(seconds=self.weapons_time) or weapon.used:
                deleting_weapons.append(weapon)
                continue
            weapon.output()
        self.delete_weapons(deleting_weapons)

    def auto_special_maneuver(self, condition):
        if condition:
            self.special_maneuver()

    def alive_check(self):
        if self.live > 0:
            return True

    def special_maneuver(self):
        pass

    def do_main_functions(self):
        pass


class MovableCharacter(Character, Movable):
    def __init__(self, screen, name, image_adress):
        Character.__init__(self, name=name)
        Movable.__init__(self, screen=screen, image_adress=image_adress)
        self.follow_x = False
        self.follow_y = False

    def follow_opponent(self, opponent):
        if self.follow_x:
            self.move_value.update({'left': opponent.rect.centerx < self.rect.centerx,
                           'right': opponent.rect.centerx > self.rect.centerx})
        if self.follow_y:
            self.move_value.update({'up': opponent.rect.centery < self.rect.centery,
                                    'down': opponent.rect.centery > self.rect.centery})

    def auto_control(self, opponent):
        self.follow_opponent(opponent)
        if opponent.live <= 0:
            self.follow_x = False
            self.follow_y = False