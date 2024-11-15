import pygame, random, sys
from pygame.locals import *
from Asteroids_Class.Enemy_Class import Asteroids
from Asteroids_Class.Enemy_Class import Space_Drones
from Asteroids_Class.Enemy_Class import Alien_Fighters
from Asteroids_Class.Enemy_Class import Bullets

TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
PLAYERMOVERATE = 5
add_new_asteroid_rate = 10
add_new_spacedrone_rate = 10
add_new_fighter_rate = 20
add_new_bullet_rate = 5 
LEVEL = 0
timer = 0 
AsteroidImage = pygame.image.load('Asteroids2.png')

def calculus(number) : 
    result = type(number/15)
    return result


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawTitle(text, font, surface, x, y):
    textobj1 = font.render(text, 1, TEXTCOLOR)
    textrect1 = textobj1.get_rect()
    textrect1.center = (x, y)
    surface.blit(textobj1, textrect1)

mouse_pressed = pygame.mouse.get_pressed()


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()

# Checks the size of the screen displaying the game to adapt.
screen_info = pygame.display.Info() 
WINDOWWIDTH, WINDOWHEIGHT = screen_info.current_w, screen_info.current_h
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('Asteroids_Music_final.wav')

# Set up images.
playerImage = pygame.image.load('Main_character_resized.png')
playerRect = playerImage.get_rect()

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawTitle('Dodger', font, windowSurface, (WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))
drawTitle('Press a key to start.', font, windowSurface, (WINDOWWIDTH // 2), (WINDOWHEIGHT // 2) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    asteroids = []
    spacedrones = []
    fighters = []
    bullets = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.

        # The game defines on what level we are playing. 

        if score < 1500 : 
            LEVEL = 1
        elif score > 1500 and score < 4500 : 
           LEVEL = 2
        elif score > 7500 : 
            LEVEL = 3


        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True
                if event.key == K_SPACE : 
                    timer = 1 
                    if len(bullets) <= add_new_bullet_rate : 
                        bullets = Bullets.CreateNewBullet(playerRect, bullets)

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False
                if event.key == K_SPACE : 
                    timer = 0 

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]

        # Add new enemies at the top of the screen, if needed.
        # It will check what level we are playing and will display the correct ennemies. 
        if LEVEL == 1 : 
            if len(asteroids) <= add_new_asteroid_rate :
                asteroids = Asteroids.CreateNewAsteroids(asteroids)
        elif LEVEL == 2 : 
            if len(spacedrones) <= add_new_spacedrone_rate : 
                spacedrones = Space_Drones.CreateNewSpaceDrones(spacedrones)
        elif LEVEL == 3 : 
            if len(fighters) <= add_new_fighter_rate : 
                fighters = Alien_Fighters.CreateNewFighter(fighters)
        
        if timer > 0 : 
            if score % 15 == 0 :  
                timer += 1 
                if len(bullets) <= add_new_bullet_rate : 
                    bullets = Bullets.CreateNewBullet(playerRect, bullets)
        

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the enemies down.
        # It checks what enemies to move according to the level. 
        if LEVEL == 1 : 
            asteroids = Asteroids.MoveAsteroids(asteroids)
        elif LEVEL == 2 : 
            spacedrones = Space_Drones.MoveSpaceDronesToPlayer(playerRect, spacedrones)
        elif LEVEL == 3 : 
            fighters = Alien_Fighters.MoveFighter(fighters)
        
            

        # Now moving the bullets.     
        bullets = Bullets.MoveBullet(bullets)

        # Delete ennemies that have fallen past the bottom.
        # Once again, checks the level.
        if LEVEL == 1 : 
            asteroids = Asteroids.DeleteAsteroids(asteroids)
        elif LEVEL == 2 : 
            spacedrones = Space_Drones.DeleteSpaceDrones(spacedrones)
        elif LEVEL == 3 : 
            fighters = Alien_Fighters.DeleteFighter(fighters)
        
        # Now deleting the bullets 
        bullets = Bullets.DeleteBullet(bullets)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each ennemy, according to the level.
        if LEVEL == 1 : 
            for a in asteroids : 
                windowSurface.blit(a['surface'], a['rect'])
        elif LEVEL == 2 : 
            for a in spacedrones : 
                windowSurface.blit(a['surface'], a['rect'])
        elif LEVEL == 3 : 
            for a in fighters :
                windowSurface.blit(a['surface'], a['rect'])



        # Drawing the Bullets 
        for a in bullets : 
            windowSurface.blit(a['surface'], a['rect'])

            
        pygame.display.update()

        # Check if any of the ennemies have hit the player.
        if LEVEL == 1 : 
            if Asteroids.playerHasHitAsteroids(playerRect, asteroids) : 
                if score > topScore : 
                    topScore = score 
                break
        elif LEVEL == 2 : 
            if Space_Drones.playerHasHitSpaceDrone(playerRect, spacedrones) : 
                if score > topScore : 
                    topScore = score 
                break 
        elif LEVEL == 3 : 
            if Alien_Fighters.playerHasHitFighter(playerRect, fighters) : 
                if score > topScore : 
                    topScore = score 
                break 

        #Check if any bullets have hit the enemies.
        #Checking what ennemies to look in relation with the level 
        if LEVEL == 1 : 
            bullets, asteroids, score = Bullets.BulletHasHitAsteroids(bullets, asteroids, score)
        elif LEVEL == 2 : 
            bullets, spacedrones, score = Bullets.BulletHasHitDrones(bullets, spacedrones, score)
        elif LEVEL == 3 : 
            bullets, fighters, score = Bullets.BulletHasHitFighter(bullets, fighters, score)
        


        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawTitle('GAME OVER', font, windowSurface, (WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))
    drawTitle('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 2), (WINDOWHEIGHT / 2) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
