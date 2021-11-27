import pygame as pg
import pygame.mouse
from player import Player
from voxel_render import VoxelRender

"""
Voxel-based render engine, created by Daniil Oschepkov

required: PyGame, NumPy, Numba, Noise (libraries) + Python 3+
"""

class App:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.res = self.width, self.height = (800, 450)
        self.screen = pg.display.set_mode(self.res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.player = Player()
        self.voxel_render = VoxelRender(self)
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

    def update(self):
        self.player.update()
        self.voxel_render.update()

    def draw(self):
        self.voxel_render.draw()
        pg.display.flip()

    def run(self):
        while True:
            self.update()
            self.draw()

            #[exit() for i in pg.event.get() if i.type == pg.QUIT]
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()

                if i.type == pg.KEYDOWN:
                    if i.key == pg.K_ESCAPE:
                        exit()

                if i.type == pg.KEYUP:
                    if i.key == pg.K_r:
                        self.voxel_render.edit_mode_switched = False
                    if i.key == pg.K_t:
                        self.player.action_executed = False

            self.clock.tick(60)
            pg.display.set_caption("FPS: " + str(int(self.clock.get_fps())))

if __name__ == "__main__":
    app = App()
    app.run()
