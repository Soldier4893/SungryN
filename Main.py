import pygame
import time
import numpy as np
from Player import Player
from Drink import Drink

# Images
snImg = pygame.image.load('./assets/sn2.png')
bobaImg = pygame.image.load('./assets/boba.png')
coffeeImg = pygame.image.load('./assets/coffee.png')

# Game variables
clock = pygame.time.Clock()
player = Player(350, 600, 40, 60, 10, snImg)
drinks_lst = []  # This will be used to store all the drinks in the game
start_time = time.time()


def redrawGameWindow(win):
    win.fill((255,255,255))  # Fills the screen with white (Refreshes the screen)
    player.draw(win)  # Draws the player to the screen
    for drink in drinks_lst:  # This will loop through all the drinks in the game
        drink.draw(win)  # This will draw the drink to the screen
    pygame.display.update() # This updates the screen so we can see our SN


if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    win = pygame.display.set_mode([700, 700])  # Set up the drawing window
    pygame.display.set_caption("HUNGRY SN")  # Set caption
    
    # Run until the user asks to quit
    run = True
    while run:
        # pygame.time.delay(100) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay
        clock.tick(60)  # This will set the FPS to 60

        # This will add a drink to the game every 2 seconds
        if time.time() - start_time > 2:
            drinks_lst.append(Drink((bobaImg, coffeeImg)))
            start_time = time.time()

        for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
            if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
                run = False  # Ends the game loop
        
        keys = pygame.key.get_pressed()  # This will return a list of all the keys that are currently being pressed
        
        # If the left arrow key is pressed and the player is not at the left edge of the screen
        if keys[pygame.K_LEFT] and player.x > player.vel:
            player.x -= player.vel

        # If the right arrow key is pressed and the player is not at the right edge of the screen
        if keys[pygame.K_RIGHT] and player.x < 680 - player.width - player.vel:
            player.x += player.vel
            
        for drink in drinks_lst:
            drink.y += drink.vel
            if drink.y > 700:
                drinks_lst.remove(drink)
                run = False
            if drink.y > 500:
                distance = tuple(np.subtract((player.x, player.y), (drink.x, drink.y)))
                if np.linalg.norm(distance) < player.r+drink.r:
                    drinks_lst.remove(drink)

        
        
        redrawGameWindow(win)  # This will redraw the game window

    pygame.quit()  # If we exit the loop this will execute and close our game
