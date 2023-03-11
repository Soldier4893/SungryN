import random as r

class Drink:
    def __init__(self, window, img, ticks):
        self.window = window
        self.img = img
        self.x = r.randint(0, 600)
        self.y = 0
        self.ticks = ticks
        self.vel = 10

