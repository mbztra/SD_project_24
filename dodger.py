import pygame, random, sys
from pygame.locals import *



class Asteroids (): 
    asteroids_min_size = 10 
    asteroids_max_size = 40
    asteroids_min_speed = 1 
    asteroids_max_speed = 8 

    def CreateNewAsteroids(a_list) : 
        asteroids_size = random.randint(Asteroids.asteroids_min_size, Asteroids.asteroids_max_size)
        newAsteroid = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - asteroids_size), 0 - asteroids_size, asteroids_size, asteroids_size), 'speed': random.randint(Asteroids.asteroids_min_speed, Asteroids.asteroids_max_speed), 'surface':pygame.transform.scale(AsteroidImage, (asteroids_size, asteroids_size)),}
        print(newAsteroid)
        print("HELLPPPPPPP")
        a_list.append(newAsteroid)
        return a_list

def MoveAsteroids (a_list2) :
    for a in a_list2:
        if not reverseCheat and not slowCheat:
            a['rect'].move_ip(0, a['speed'])
        elif reverseCheat:
            a['rect'].move_ip(0, -5)
        elif slowCheat:
            a['rect'].move_ip(0, 1)
    
def DeleteAsteroids(asteroids_list2) :
    for a in asteroids_list2[:] :
        if a['rect'].top > WINDOWHEIGHT:
            asteroids_list2.remove(a)


def PlayerHasHitAsteroid(playerRect, asteroids_list) : 
    for a in asteroids_list:
        if playerRect.colliderect(a['rect']):
            return True 
        else : 
            return False
    
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
add_new_asteroid_rate = 6
PLAYERMOVERATE = 5


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

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')
AsteroidImage = pygame.image.load('Asteroids.png')

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    #baddies = []
    asteroids = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    asteroids_add_counter = 0 

    

    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.
        print(score)

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

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            asteroids_add_counter += 1 
            if len(asteroids) < add_new_asteroid_rate :
               asteroids = Asteroids.CreateNewAsteroids(asteroids)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
        
        #Move the asteroids down : 
        MoveAsteroids(asteroids)

        # Delete the asteroids : 
        DeleteAsteroids(asteroids)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)
        
        # Draw each asteroid : 
        for a in asteroids : 
            windowSurface.blit(a['surface'], a['rect'])

        pygame.display.update()


        #Check if any asteroids have hit the player : 
        if PlayerHasHitAsteroid(playerRect, asteroids) : 
            if score > topScore : 
                topScore = score 
            break 

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
