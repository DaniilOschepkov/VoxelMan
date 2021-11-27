import pygame as pg
from numba import njit
import numpy as np
import math
from noise_generator import NoiseGenerator
from globals import *

# noise generator which allows to generate good noises
noiseGenerator = NoiseGenerator()
# other settings
height_map = noiseGenerator.perlin_noise((600,600))

map_height = len(height_map[0])
map_width = len(height_map)

def edit(size, x, y):
    edit_map = np.zeros(MAP_SIZE)
    for i in range(y, y+size):
        for j in range(x, x+size):
            edit_map[j, i] = 1

    return edit_map

def destroy_part(size, x, y):
    for i in range(y, y+size):
        for j in range(x, x+size):
            height_map[j, i] = 0


@njit(fastmath=True)
def ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch, screen_width,screen_height,delta_angle,ray_distance,h_fov,scale_height, edit_mode, edit_map, enable_water):

    screen_array[:] = np.array([0,0,0])
    y_buffer = np.full(screen_width,screen_height)

    ray_angle = player_angle - h_fov
    for num_ray in range(screen_width):
        first_contact = False
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        for depth in range(1, ray_distance):
            x = int(player_pos[0] + depth * cos_a)
            if 0 < x < map_width:
                y = int(player_pos[1] + depth * sin_a)
                if 0 < y < map_height:

                    depth *= math.cos(player_angle - ray_angle)
                    height_on_screen = int((player_height - height_map[x, y]*100) / depth * scale_height + player_pitch)

                    if not first_contact:
                        y_buffer[num_ray] = min(height_on_screen, screen_height)
                        first_contact = True

                    if height_on_screen < 0:
                        height_on_screen = 0

                    if height_on_screen < y_buffer[num_ray]:
                        for screen_y in range(height_on_screen, y_buffer[num_ray]):
                            green = height_map[x,y]*100
                            screen_array[num_ray, screen_y] = (0, int(green), 0)

                            if enable_water and green < 40:
                                screen_array[num_ray, screen_y] = WATER_COLOR

                            if edit_mode:
                                if edit_map[x,y] == 1:
                                    screen_array[num_ray, screen_y] = (255, 0, 0)


                        y_buffer[num_ray] = height_on_screen

        ray_angle += delta_angle


    return screen_array

class VoxelRender:

    def __init__(self, app):
        self.app = app
        self.player = app.player

        # raycasting stuff
        self.fov = math.pi / 3
        self.h_fov = self.fov / 2
        self.num_rays = app.width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = 2000
        self.scale_height = 620
        self.screen_array = np.full((app.width,app.height,3), (0,0,0))
        self.edit_mode = False
        self.edit_mode_switched = False
        self.editX = 0
        self.editY = 0
        self.editSpeed = 6
        self.edit_rect_size = EDIT_RECT_SIZE

    def update(self):
        self.edit_map = edit(self.edit_rect_size, self.editX, self.editY)
        self.screen_array = ray_casting(self.screen_array, self.player.pos, self.player.angle, self.player.height,self.player.pitch,self.app.width,self.app.height,self.delta_angle,self.ray_distance,self.h_fov,self.scale_height,self.edit_mode, self.edit_map, self.player.enable_water)

        pressed_key = pg.key.get_pressed()

        if pressed_key[pg.K_r] and not (self.edit_mode_switched):
            self.edit_mode_switched = True
            if self.edit_mode:
                self.edit_mode = False
                print("edit mode disabled")
            else:
                self.edit_mode = True
                print("edit mode enabled")

        # edit mode control
        if pressed_key[pg.K_UP]:
            self.editY += self.editSpeed
        if pressed_key[pg.K_DOWN]:
            self.editY -= self.editSpeed
        if pressed_key[pg.K_RIGHT]:
            self.editX += self.editSpeed
        if pressed_key[pg.K_LEFT]:
            self.editX -= self.editSpeed

        if pressed_key[pg.K_SPACE] and self.edit_mode:
            destroy_part(self.edit_rect_size, self.editX, self.editY)

    def draw(self):
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array), (0,0))