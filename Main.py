import pygame, time
import numpy as np
from Player import Player
from Drink import Drink
import button

# Initialize pygame
pygame.init()
win = pygame.display.set_mode([700, 700])  # Set up the drawing window
pygame.display.set_caption("HUNGRY SN")  # Set caption

# Images for game objects
snImg = pygame.image.load('./assets/sn2.png')
bobaImg = pygame.image.load('./assets/boba.png')
coffeeImg = pygame.image.load('./assets/coffee.png')

# load button images
resume_img = pygame.image.load("button_images/button_resume.png").convert_alpha()
options_img = pygame.image.load("button_images/button_options.png").convert_alpha()
quit_img = pygame.image.load("button_images/button_quit.png").convert_alpha()
back_img = pygame.image.load('button_images/button_back.png').convert_alpha()

# create button instances
resume_button = button.Button(50, 150, resume_img, 1)
credits_button = button.Button(50, 275, options_img, 1)
quit_button = button.Button(50, 400, quit_img, 1)
back_button = button.Button(332, 450, back_img, 1)

# Game variables
clock = pygame.time.Clock()
player = Player(350, 600, 40, 60, 10, snImg)
drinks_lst = []  # This will be used to store all the drinks in the game
start_time = time.time()
font = pygame.font.SysFont('comicsans', 30, bold=True, italic=False)
SCORE = 0
LIVES = 3
DIFFICULTY = 1
TEXT_COL = (255, 255, 255)
menu_state = "main"
game_has_started = False

# Function to draw text to the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  win.blit(img, (x, y))


def redrawGameWindow(win):
    win.fill((255,255,255))  # Fills the screen with white (Refreshes the screen)

    # Drawing the player and drink objects to the screen
    player.draw(win)
    for drink in drinks_lst:  
        drink.draw(win)

    # Draw the score to the screen
    draw_text("Score: " + str(SCORE), font, (0,0,0), 10, 10)

    # Draw lives to the screen
    draw_text("Lives: " + str(LIVES), font, (0,0,0), 10, 50)
    
    # If the game is over, draw the game over text to the screen
    if LIVES == 0:
        draw_text("GAME OVER!", font, (0,0,0), 250, 350)

    pygame.display.update() # This updates the screen so we can see our SN

if __name__ == "__main__":    
    # Run until user runs out of lives
    run = True
    while run:
        #event handler loop (check if user has quit the game)
        for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
            if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
                run = False  # Ends the game loop

        #check if game is paused
        if not game_has_started:
            win.fill((0,0,0))

            #check menu state
            if menu_state == "main":
                #draw pause screen buttons
                if resume_button.draw(win):
                    game_has_started = True
                if credits_button.draw(win):
                    menu_state = "credits"
                if quit_button.draw(win):
                    run = False
            #check if the credits menu is open
            if menu_state == "credits":
                #draw credits screen
                if back_button.draw(win):
                    menu_state = "main"

            pygame.display.update()  # This updates the screen


        if game_has_started:
            # pygame.time.delay(100) # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay
            clock.tick(60)  # This will set the FPS to 60

            # If the player runs out of lives, remove all the drinks from the game
            if LIVES == 0:
                drinks_lst = []

            # This will add a drink to the game every 2 seconds (decreases with difficulty) if the game is not over
            if time.time() - start_time > 0.1+2/DIFFICULTY and LIVES > 0:
                drinks_lst.append(Drink((bobaImg, coffeeImg)))
                start_time = time.time()
                if DIFFICULTY < 50:
                    DIFFICULTY += 0.2

            keys = pygame.key.get_pressed()  # This will return a list of all the keys that are currently being pressed
            
            # If the left arrow key is pressed and the player is not at the left edge of the screen
            if keys[pygame.K_LEFT] and player.x > player.vel:
                player.x -= player.vel

            # If the right arrow key is pressed and the player is not at the right edge of the screen
            if keys[pygame.K_RIGHT] and player.x < 680 - player.width - player.vel:
                player.x += player.vel
            
            # Code to move the drinks down the screen
            for drink in drinks_lst:
                drink.y += drink.vel
                if drink.y > 700:
                    drinks_lst.remove(drink)
                    LIVES -= 1
                # If the drink hits the player, remove the drink from the game and add 1 to the score
                if drink.y > 500:
                    distance = tuple(np.subtract((player.x, player.y), (drink.x, drink.y)))
                    if np.linalg.norm(distance) < player.r + drink.r:
                        drinks_lst.remove(drink)
                        SCORE += 1

            redrawGameWindow(win)  # This will redraw the game window

    pygame.quit()  # If we exit the loop this will execute and close our game
