import pygame as pg
import numpy as np
import math

from globals import *

import pygame.mouse


class Player:
    def __init__(self):
        self.pos = np.array([0,0], dtype=float)
        self.angle = math.pi / 4
        self.height = 270
        self.pitch = 40
        self.vel = 3
        self.rotate_coeff = 0.01
        self.rotate_y_coeff = 2
        self.height_speed = 3
        self.vel_multiplier = 0;
        self.vel_multiplier_value = 4
        self.enable_water = False
        self.action_executed = False

    def update(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        # controls with keyboard-mouse
        pressed_key = pg.key.get_pressed()

        # rotation
        mouseX, mouseY = pygame.mouse.get_rel()

        self.angle += mouseX * self.rotate_coeff
        self.pitch -= mouseY * self.rotate_y_coeff

        # movement
        if pressed_key[pg.K_w]:
            self.pos[0] += (self.vel + self.vel_multiplier) * cos_a
            self.pos[1] += (self.vel + self.vel_multiplier) * sin_a
        if pressed_key[pg.K_s]:
            self.pos[0] -= (self.vel + self.vel_multiplier) * cos_a
            self.pos[1] -= (self.vel + self.vel_multiplier) * sin_a
        if pressed_key[pg.K_a]:
            self.pos[0] += (self.vel + self.vel_multiplier) * sin_a
            self.pos[1] -= (self.vel + self.vel_multiplier) * cos_a
        if pressed_key[pg.K_d]:
            self.pos[0] -= (self.vel + self.vel_multiplier) * cos_a
            self.pos[1] += (self.vel + self.vel_multiplier) * sin_a

        if pressed_key[pg.K_e]:
            self.height += self.height_speed
        if pressed_key[pg.K_q]:
            self.height -= self.height_speed

        if pressed_key[pg.K_z]:
            self.vel_multiplier = self.vel_multiplier_value
        else:
            self.vel_multiplier = 0

        # enable-disable water
        if pressed_key[pg.K_t] and not self.action_executed:
            self.action_executed = True
            self.enable_water = not self.enable_water