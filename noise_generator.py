import pygame as pg
import numpy as np
import noise
from noise import pnoise2
from globals import *

class NoiseGenerator:
    def __init__(self):
        pass

    def perlin_noise(self, shape = MAP_SIZE, scale = 300, octaves = 6, persistence = 0.5, lacunarity = 2.0, seed = None):
        if not seed:
            seed = np.random.randint(0,100)

        arr = np.zeros(shape)

        for i in range(shape[0]):
            for j in range(shape[1]):
                arr[i][j] = pnoise2(i / scale, j / scale, octaves = octaves, persistence = persistence, lacunarity = lacunarity, repeatx = 1024, repeaty = 1024, base = seed)


        max_arr = np.max(arr)
        min_arr = np.min(arr)
        norm_me = lambda x: (x - min_arr) / (max_arr - min_arr)
        norm_me = np.vectorize(norm_me)
        arr = norm_me(arr)
        return arr