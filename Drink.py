import random as r

class Drink:
    def __init__(self, img_tuple):
        self.img = img_tuple[r.randint(0, len(img_tuple) - 1)]
        self.x = r.randint(0, 600)
        self.y = 0
        self.vel = 6
        self.r = 4

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))