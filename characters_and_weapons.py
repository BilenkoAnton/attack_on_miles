import datetime
import random
import time
from copy import copy

import pygame

from audio import weapon_effect
from objects_template import MovableCharacter, Movable, Weapon


class Rhino(MovableCharacter):
    def __init__(self, screen):
        super().__init__(screen, 'Rhino', 'images/right_rhino.png')
        self.rect.left = self.screen_rect.left
        self.rect.centery = self.screen_rect.centery
        self.left_image = 'images/left_rhino.png'
        self.normal_speed = copy(self.speed)
        self.super_speed = 4
        self.damage = 40
        self.follow_y = True

    def special_maneuver(self):
        self.speed = self.super_speed
        self.move_value.update({attitude: False for attitude in self.move_value})
        self.move_value.update({self.actual_attitude: True})

    def damage_opponent(self, opponent):
        if self.speed == self.super_speed and self.rect.colliderect(opponent):
            opponent.live -= self.damage
            self.stop_maneuver()
            weapon_effect('rhino')

    def horizon_check(self):
        if any((self.rect.right >= self.screen_rect.right,
                self.rect.left <= self.screen_rect.left)):
            return True

    def stop_maneuver(self):
        self.move_value.update({'right': False, 'left': False})
        self.speed = self.normal_speed

    def speed_working(self):
        if self.speed == self.super_speed:
            if len(tuple(move for move in self.move_value.values() if move)) != 1 or self.horizon_check():
                self.stop_maneuver()

    def auto_control(self, opponent):
        super().auto_control(opponent)
        if self.rect.centery == opponent.rect.centery and self.horizon_check() and opponent.live >= 0:

            self.follow_y = False
            self.special_maneuver()
        elif not self.horizon_check() and self.speed == self.normal_speed:
            self.move_value.update({'left': True})
        if any((self.actual_attitude == 'right' and self.rect.right >= self.screen_rect.right,
                self.actual_attitude == 'left' and self.rect.left <= self.screen_rect.left)):
            self.move_value.update({attitude: False for attitude in self.move_value})
            self.turn_around(mustable_turn=True)
            self.follow_y = True

    def do_main_functions(self):
        self.move()
        self.speed_working()
        self.output()


class Miles(MovableCharacter):
    def __init__(self, screen):
        super().__init__(screen, 'Miles', 'images/right_miles.png')
        self.rect.center = self.screen_rect.center
        self.speed = 3
        self.left_image = 'images/left_miles.png'
        self.dead_image = 'images/dead_miles.png'
        self.auto_mod = False

    def damage_opponent(self, opponent):
        pass

    def auto_control(self, opponent):
        random_value = random.choice(list(self.move_value.keys()))
        if self.move_value.get(random_value):
            self.move_value.update({random_value: False})
        else:
            self.move_value.update({random_value: True})

    def do_main_functions(self):
        if self.alive_check():
            self.move()
        elif self.image_adress != self.dead_image:
            self.image_adress = self.dead_image
            self.left_image = self.dead_image
            self.image = pygame.image.load(self.image_adress)
            actual_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = actual_center
        self.output()


class Kraven(MovableCharacter):
    def __init__(self, screen):
        super().__init__(screen, 'Kraven', 'images/right_kraven.png')
        self.rect.topleft = self.screen_rect.topleft
        self.left_image = 'images/left_kraven.png'
        self.follow_y = True

    def special_maneuver(self):
        spear = Spear(self.screen, self.rect, self)
        if self.actual_attitude == 'left':
            spear.rect.right = self.rect.left
            spear.move_value.update({'left': True, 'right': False})
        self.weapon_list.add(spear)

    def damage_opponent(self, opponent):
        for spear in self.weapon_list:
            spear.damage_opponent(opponent)

    def work_with_weapons(self):
        super().work_with_weapons()
        for spear in self.weapon_list:
            spear.move()

    def auto_control(self, opponent):
        super().auto_control(opponent)
        if any((self.rect.centery == opponent.rect.bottom, self.rect.centery == opponent.rect.top)) and opponent.live >= 0:
            self.special_maneuver()

    def do_main_functions(self):
        self.move()
        self.work_with_weapons()
        self.output()


class Electro(MovableCharacter):
    def __init__(self, screen):
        super().__init__(screen, 'Electro', 'images/electro.png')
        self.rect.bottomright = self.screen_rect.bottomright
        self.damage = 50
        self.weapons_time = 2
        self.follow_x = True
        self.follow_y = True

    def special_maneuver(self):
        if not self.weapon_list:
            weapon_effect('electro')
            self.weapon_list.add(FlashBang(self.screen, self))

    def damage_opponent(self, opponent):
        for flash in self.weapon_list:
            flash.damage_opponent(opponent)

    def auto_control(self, opponent):
        super().auto_control(opponent)
        if all((abs(self.rect.centerx-opponent.rect.centerx) <= 100,
                abs(self.rect.centery-opponent.rect.centery) <= 100,
               opponent.live >= 0)):
            self.special_maneuver()

    def do_main_functions(self):
        self.work_with_weapons()
        if not self.weapon_list:
            self.move()
        self.output()


class Mysterio(MovableCharacter):
    def __init__(self, screen):
        super().__init__(screen, 'Mysterio', 'images/mysterio.png')
        self.rect.topright = self.screen_rect.topright
        self.mysterio_world = False
        self.number_of_clones = 10
        self.clones_list = set()
        self.time_into_world = 10

    def create_coordinates(self):
        coordinate_x = random.choice(range(self.rect.width//2, self.screen_rect.right - self.rect.width//2))
        coordinate_y = random.choice(range(self.rect.height//2, self.screen_rect.bottom - self.rect.height//2))
        return coordinate_x, coordinate_y

    def special_maneuver(self):
        smoke = Smoke(self.screen, self)
        smoke.rect.x, smoke.rect.y = self.create_coordinates()
        self.weapon_list.add(smoke)

    def work_with_weapons(self):
        if self.mysterio_world:
            self.weapon_list = {weapon for weapon in self.weapon_list if type(weapon) != Smoke}
            for weapon in self.weapon_list:
                weapon.move()
        super().work_with_weapons()

    def damage_opponent(self, opponent):
        for weapon in self.weapon_list:
            weapon.damage_opponent(opponent)
        if self.mysterio_world:
            if self.rect.colliderect(opponent):
                self.live -= opponent.damage
                self.clones_list.clear()
                self.mysterio_world = False
            if self.clones_list and datetime.datetime.now() - min((clone.date_of_create for clone in self.clones_list)) > datetime.timedelta(seconds=self.time_into_world):
                self.mega_punch(opponent)
                self.clones_list.clear()

    def make_a_clones(self):
        for clone in range(self.number_of_clones):
            self.clones_list.add(MysteriosClone(self.screen))

    def hide(self):
        self.rect.x, self.rect.y = self.create_coordinates()

    def mega_punch(self, opponent: Miles):
        opponent.stoppable = True
        fist = BigHand(self.screen, self)
        fist.rect.bottom = fist.rect.top
        fist.rect.centerx = opponent.rect.centerx
        self.weapon_list.add(fist)

    def auto_control(self, opponent):
        super().auto_control(opponent)
        if not self.weapon_list and not self.clones_list:
            self.special_maneuver()

    def do_main_functions(self):
        if not self.mysterio_world:
            self.move()
        elif {weapon for weapon in self.weapon_list if type(weapon) == Smoke}:
            self.weapon_list.clear()
        self.output()
        self.work_with_weapons()
        for clone in self.clones_list:
            clone.output()


class Spear(Weapon, Movable):
    def __init__(self, screen, character_rect, owner: Kraven):
        Weapon.__init__(self, owner, screen, 'images/right_spear.png')
        Movable.__init__(self, screen, 'images/right_spear.png')
        self.move_value.update({'right': True})
        self.rect.left = character_rect.right
        self.rect.centery = character_rect.centery
        self.left_image = 'images/left_spear.png'
        self.speed = 2
        self.damage = 30

    def damage_opponent(self, character):
        if self.rect.colliderect(character):
            character.live -= self.damage
            self.used = True
            weapon_effect('spear')


class FlashBang(Weapon):
    def __init__(self, screen, owner: Electro):
        Weapon.__init__(self, owner, screen, 'images/flash_bang_2.png')
        self.rect.center = owner.rect.center
        self.damage = 0.3

    def damage_opponent(self, opponent):
        super().damage_opponent(opponent)
        self.used = False


class Smoke(Weapon):
    def __init__(self, screen, owner: Mysterio):
        Weapon.__init__(self, owner, screen, 'images/smoke.png')
        self.damage = 0

    def damage_opponent(self, opponent):
        if self.rect.colliderect(opponent) and not self.used:
            self.owner.mysterio_world = True
            weapon_effect('mysterio_laugh')
            time.sleep(3)
            self.owner.make_a_clones()
            self.owner.hide()


class MysteriosClone(Mysterio):
    def __init__(self, screen):
        Mysterio.__init__(self, screen)
        self.rect.center = self.create_coordinates()


class BigHand(Weapon, Movable):
    def __init__(self, screen, owner: Mysterio):
        Weapon.__init__(self, owner, screen, 'images/big_hand.png')
        Movable.__init__(self, screen, 'images/big_hand.png')
        self.damage = 40
        self.move_value.update({'down': True})

    def damage_opponent(self, opponent):
        super().damage_opponent(opponent)
        if self.used:
            self.owner.mysterio_world = False
            opponent.stoppable = False
            weapon_effect('punch')
