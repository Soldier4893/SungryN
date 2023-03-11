class Player(object):
    def __init__(self, x, y, width, height, vel, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.img = img

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))