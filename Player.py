import pygame as pg
class Player(object):
    def __init__(self, x, y, width, height, vel, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.img = img
        self.r = 64
        self.img2 = pg.transform.flip(self.img, True, False)

    def draw(self, win, direction):
        if direction == 0:
            win.blit(self.img, (self.x, self.y))
        else:
            win.blit(self.img2, (self.x, self.y))