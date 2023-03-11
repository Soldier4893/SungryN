import pygame as pg
import time
import numpy as np
from Player import Player
from Drink import Drink

# Initialize pg
pg.init()
win = pg.display.set_mode([700, 700])  # Set up the drawing window
pg.display.set_caption("SUNGRYN")  # Set caption

# Images
snImg = pg.image.load('./assets/sn2.png')
bobaImg = pg.image.load('./assets/boba.png')
coffeeImg = pg.image.load('./assets/coffee.png')
backgroundImg = pg.image.load('./assets/background.png')

# Game variables
clock = pg.time.Clock()
player = Player(350, 600, 40, 60, 10, snImg)
drinks_lst = []  # This will be used to store all the drinks in the game
start_time = time.time()
font = pg.font.SysFont('comicsans', 30, bold=True, italic=False)
SCORE = 0
LIVES = 3
DIFFICULTY = 1
DIRECTION = 0


def redrawGameWindow(win, direction):
    win.fill((255,255,255))  # Fills the screen with white (Refreshes the screen)

    # Draw background
    win.blit(backgroundImg, (0, 0))
    
    # Drawing the player and drink objects to the screen
    player.draw(win, direction)
    for drink in drinks_lst:  
        drink.draw(win)

    # Draw the score to the screen
    text = font.render("Score: " + str(SCORE), 1, (0,0,0))
    win.blit(text, (10, 10))
    # Draw lives to the screen
    text = font.render("Lives: " + str(LIVES), 2, (0,0,0))
    win.blit(text, (10, 50))
    # If the game is over, draw the game over text to the screen
    text = font.render("GAME OVER!", 1, (0,0,0))
    if LIVES == 0:
        win.blit(text, (250, 350))  

    pg.display.update() # This updates the screen so we can see our SN

if __name__ == "__main__":    
    
    direction = 0
    
    # Music
    pg.mixer.init()
    pg.mixer.music.load("./assets/score.mp3")
    pg.mixer.music.set_volume(0.3)
    pg.mixer.music.play(-1)
    
    # Run until user runs out of lives
    run = True
    while run:
        # pg.time.delay(100) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay
        clock.tick(60)  # This will set the FPS to 60

        # If the player runs out of lives, remove all the drinks from the game
        if LIVES == 0:
            pg.mixer.music.pause()
            drinks_lst = []

        # This will add a drink to the game every 2 seconds (decreases with difficulty) if the game is not over
        if time.time() - start_time > 0.1+2/DIFFICULTY and LIVES > 0:
            drinks_lst.append(Drink((bobaImg, coffeeImg)))
            start_time = time.time()
            if DIFFICULTY < 50:
                DIFFICULTY += 0.2
            

        for event in pg.event.get():  # This will loop through a list of any keyboard or mouse events.
            if event.type == pg.QUIT: # Checks if the red button in the corner of the window is clicked
                run = False  # Ends the game loop
        
        keys = pg.key.get_pressed()  # This will return a list of all the keys that are currently being pressed
        
        # If the left arrow key is pressed and the player is not at the left edge of the screen
        if keys[pg.K_LEFT] and player.x > player.vel:
            direction = 0
            player.x -= player.vel

        # If the right arrow key is pressed and the player is not at the right edge of the screen
        if keys[pg.K_RIGHT] and player.x < 680 - player.width - player.vel:
            direction = 1
            player.x += player.vel
        
        # Code to move the drinks down the screen
        for drink in drinks_lst:
            drink.y += drink.vel
            if drink.y > 700:
                drinks_lst.remove(drink)
                LIVES -= 1
            if drink.y > 500:
                distance = tuple(np.subtract((player.x, player.y), (drink.x, drink.y)))
                if np.linalg.norm(distance) < player.r + drink.r:
                    drinks_lst.remove(drink)
                    SCORE += 1

        redrawGameWindow(win, direction)  # This will redraw the game window

    pg.quit()  # If we exit the loop this will execute and close our game
