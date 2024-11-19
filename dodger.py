import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

# Initialize Pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Galaxy Guardian')
pygame.mouse.set_visible(False)

# Set up fonts and sounds
font = pygame.font.SysFont(None, 48)
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Load images
playerImage = pygame.image.load('ufo.png')
baddieImage = pygame.image.load('baddie.png')

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
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
    textrect.midtop = (WINDOWWIDTH / 2, y)
    surface.blit(textobj, textrect)

class Player:
    def __init__(self, image, x, y, speed=PLAYERMOVERATE, lives=3):
        self.image = image
        self.rect = image.get_rect(center=(x, y))
        self.speed = speed
        self.lives = lives
        self.help_used = False

    def move(self, moveLeft, moveRight, moveUp, moveDown):
        if moveLeft and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if moveRight and self.rect.right < WINDOWWIDTH:
            self.rect.move_ip(self.speed, 0)
        if moveUp and self.rect.top > 0:
            self.rect.move_ip(0, -self.speed)
        if moveDown and self.rect.bottom < WINDOWHEIGHT:
            self.rect.move_ip(0, self.speed)

    def lose_life(self):
        self.lives -= 1
        print(f"Lives left: {self.lives}")
        if self.lives <= 0:
            terminate()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Show the "Start" screen
# windowSurface.fill(BACKGROUNDCOLOR)
# drawText('Galaxy Guardian', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
# drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
# pygame.display.update()
# waitForPlayerToPressKey()

# Load the background image
backgroundImage = pygame.image.load('space.jpg')  # Replace 'background.jpg' with your image file

# Scale the image to fit the window if necessary
backgroundImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))

# Show the "Start" screen with the background image
windowSurface.blit(backgroundImage, (0, 0))  # Draw the image at the top-left corner of the screen
drawText('Galaxy Guardian', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    player = Player(playerImage, WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # Game loop
        score += 1 # Increase score

        # Event handling
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
# Add new baddies
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize))}
            baddies.append(newBaddie)

        # Move the player
        player.move(moveLeft, moveRight, moveUp, moveDown)

        # Move the baddies
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)
        # Remove baddies that have fallen past the bottom
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the background and player
        # windowSurface.fill(BACKGROUNDCOLOR)
        # drawText(f'Score: {score}', font, windowSurface, 10, 0)
        # drawText(f'Top Score: {topScore}', font, windowSurface, 10, 40)
        # player.draw(windowSurface)

        windowSurface.blit(backgroundImage, (0, 0))  # Draw the background image
        drawText(f'Score: {score}', font, windowSurface, 10, 0)
        drawText(f'Top Score: {topScore}', font, windowSurface, 10, 40)
        player.draw(windowSurface)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check collisions
        if playerHasHitBaddie(player.rect, baddies):
            if score > topScore:
                topScore = score
            break

        mainClock.tick(FPS)

    # Show Game Over screen
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()