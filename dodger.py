import pygame, random, sys
from pygame.locals import *
from Asteroids_Class.Enemy_Class import *

# Defining all the important variables for later 
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
PLAYERMOVERATE = 5
add_new_bullet_rate = 5 
add_new_falcon_rate = 1
add_new_boss_rate = 1 
helpers_rate = 2
limitless_rate = 3
LEVEL = 0
facing = 1 
timer = 0 
helper_timer = 0 
helper_check = 0
limitless = False
call_for_help = False
AsteroidImage = pygame.image.load('Asteroids2.png')
pause = False
LVL = 0  
boss_facing = "left"
difficulty = 0 
boss_dead = False 

# Defining a few important functions 
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

def draw_box_with_text(screen, text, x, y, width, height, font): 
    words = text.split(' ') 
    lines = [] 
    current_line = words[0] 

    for word in words[1:]: 
        # Check if the current line with the next word fits within the box width 
        if font.size(current_line + ' ' + word)[0] <= width - 20: 
            # Add some padding 
            current_line += ' ' + word 
        else: 
            lines.append(current_line) 
            current_line = word 
    lines.append(current_line) 

    total_text_height = len(lines) * font.get_height()
    start_y = y + (height - total_text_height) // 2

    pygame.draw.rect(screen, (0,0,0), (x, y, width, height)) 
    pygame.draw.rect(screen, (255,255,255), (x, y, width, height), 2) 
    # Render each line and blit it to the screen
    for i, line in enumerate(lines): 
        text_surface = font.render(line, True, (255,255,255)) 
        text_rect = text_surface.get_rect(center=(x + width // 2, start_y + i * font.get_height()))
        # Adjust the position with some padding 
        screen.blit(text_surface, text_rect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()

# Checks the size of the screen displaying the game to adapt.
screen_info = pygame.display.Info() 
WINDOWWIDTH, WINDOWHEIGHT = screen_info.current_w, screen_info.current_h
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

#Defines the name of the window 
pygame.display.set_caption('Galaxy Guardian')
pygame.mouse.set_visible(False)

# Set up the fonts.
font_path = 'Orbitron-Regular.ttf'  # Path to your custom font in the project folder
font = pygame.font.Font(font_path, 30)  # Load the custom font with a size of 48
font_title = pygame.font.Font(font_path, 50)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('laser.wav')
pygame.mixer.music.load('Asteroids_Music_final.wav')


# Set up images.
playerImage = pygame.image.load('Main_character_resized.png')
playerRect = playerImage.get_rect()
backgroundImage = pygame.image.load('space.jpg')  # Replace 'background.jpg' with your image file
backgroundImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
logoImage = pygame.image.load("Logo2.png")
image_width, image_height = logoImage.get_size() # Calculate the position to center the image 
x_pos = (WINDOWWIDTH - image_width) / 2 
y_pos = (WINDOWHEIGHT - image_height) / 2 - 100
Boss_image = pygame.image.load('Boss-ship.png')
Boss_width, Boss_height = Boss_image.get_size()
y_final_pos = -Boss_width/25 + 50


# Show the "Start" screen.
windowSurface.blit(backgroundImage, (0, 0))  # Draw the image at the top-left corner of the screen
windowSurface.blit(logoImage, (x_pos, y_pos ))
drawTitle('Galaxy Guardian', font_title, windowSurface, (WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))
drawTitle('Press a key to start.', font, windowSurface, (WINDOWWIDTH // 2), (WINDOWHEIGHT // 2) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True : 
    # Set up the start of the game.

    # Set up the lists of all ennemies 
    asteroids = []
    spacedrones = []
    fighters = []
    bullets = []
    mean_bullets = []
    falcons = []
    boss = []
    helpers = []
    boss_bullets = []
    boss_missiles = []

    #Set up Score and Player 
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)

    #Set up the movement and music 
    moveLeft = moveRight = moveUp = moveDown = False
    pygame.mixer.music.play(-1, 0.0)
    volume = 1
    pygame.mixer.music.set_volume(volume)

    #set up difficulty 

    while True: # The game loop runs while the game part is playing.
        if not LEVEL == "To Boss" and not LEVEL == "To level 2" and not LEVEL == "To level 3" and not LEVEL == 5 and not LEVEL == "PAUSE":
            score += 1  # Increase score.
        if not helper_timer == 0 : 
            helper_timer += 1 
        #Randomizes the chance to get the Easter Egg
        falcon_test = random.randint(1, 3000) 

        # The game defines on what level we are playing. 
        if pause : 
            LVL = LEVEL
            LEVEL = "PAUSE"
        elif score < 1500 and not LEVEL == 0 : 
            LEVEL = 1
        elif score > 1500 and score < 1510 : 
            LEVEL = "To level 2"
        elif score > 1510 and score < 4500 : 
           LEVEL = 2
        elif score > 4500 and score < 4510 : 
            LEVEL = "To level 3"
        elif score > 4510 and score < 7500 : 
            LEVEL = 3
        elif score > 7500 and score < 7510 : 
            LEVEL = "To Boss"
        elif score > 7510 and not LEVEL == 5 and not LEVEL == 6 and not LEVEL == "PAUSE" : 
            LEVEL = 4
        elif score > 7510 and boss_dead and not LEVEL == 5 : 
            LEVEL = 6 

        # We now check for every action possible 

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a :
                    if not LEVEL == "PAUSE" : 
                        moveRight = False
                        moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    if not LEVEL == "PAUSE" :
                        moveLeft = False
                        moveRight = True
                if event.key == K_UP or event.key == K_w:
                    if not LEVEL == "PAUSE" :
                        moveDown = False
                        moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    if not LEVEL == "PAUSE" :
                        moveUp = False
                        moveDown = True
                if event.key == K_SPACE : 
                    # Create a timer to able the player to keep shooting
                    timer = 1 
                    if len(bullets) <= add_new_bullet_rate : 
                        bullets = Bullets.CreateNewBullet(playerRect, bullets, False)
                if event.key == K_RETURN : 
                    if LEVEL == "To level 2" : 
                        LEVEL = 2 
                        score = 1510
                    elif LEVEL == "To level 3" : 
                        LEVEL = 3 
                        score = 4510
                    elif LEVEL == "To Boss" : 
                        LEVEL = 4
                        score = 7510
                    if limitless : 
                        LEVEL = 6
                        asteroids = []
                        spacedrones = []
                        fighters = []
                        mean_bullets = []
                if event.key == K_h : 
                    call_for_help = True 
                if event.key == K_LCTRL : 
                    if pause == True : 
                        pause = False
                        LEVEL = LVL
                    else : 
                        pause = True 
                if LEVEL == 0 : 
                    if event.key == K_1:  
                            difficulty = 1 
                            LEVEL = 1 
                    if event.key == K_2 :  
                            difficulty = 2
                            LEVEL = 1  
                    if event.key == K_3 : 
                            difficulty = 3
                            LEVEL = 1  

            if event.type == KEYUP:
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
                    # Reinitialise the timer so the player stops shooting
                    timer = 0 

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        
        if difficulty == 1 : 
            add_new_asteroid_rate = 5
            add_new_spacedrone_rate = 3
            add_new_fighter_rate = 5 
        elif difficulty == 2 : 
            add_new_asteroid_rate = 10
            add_new_spacedrone_rate = 7
            add_new_fighter_rate = 10
        elif difficulty == 3 : 
            add_new_asteroid_rate = 20
            add_new_spacedrone_rate = 14
            add_new_fighter_rate = 20

        # Add new enemies at the top of the screen, if needed.
        # It will check what level we are playing and will display the correct ennemies. 
        if LEVEL == 1 : 
            if len(asteroids) <= add_new_asteroid_rate :
                asteroids = Asteroids.CreateNewAsteroids(asteroids)
            if falcon_test == 9 and len(falcons) < add_new_falcon_rate : 
                falcons = millenium_falcon.CreateNewFalcon(falcons)
        elif LEVEL == 2 : 
            if len(spacedrones) <= add_new_spacedrone_rate : 
                spacedrones = Space_Drones.CreateNewSpaceDrones(spacedrones)
        elif LEVEL == 3 : 
            if len(fighters) <= add_new_fighter_rate : 
                fighters = Alien_Fighters.CreateNewFighter(fighters)
            if score % 60  == 0 : 
                enemy_bullets = EnemyBullets.EnemiesShoot(fighters, mean_bullets)
        elif LEVEL == 4 : 
            if len(boss) < add_new_boss_rate : 
                boss = BossShip.CreateNewBoss(boss)
            if score % 30 == 0 : 
                boss_bullets = BossBullets.BossShoot(boss_bullets, boss)
                if len(boss_missiles) < 2 : 
                    boss_missiles = BossBombs.BossShootsBombs(boss_missiles, boss, 2)
                    facing = 2
                elif facing == 2 :  
                    boss_missiles = BossBombs.BossShootsBombs(boss_missiles, boss, 1)
                    facing = 1 
            if call_for_help : 
                if len(helpers) < helpers_rate and helper_check == 0 : 
                    helpers = Helpers.CallForHelpers(helpers, boss, 0)
                    helpers = Helpers.CallForHelpers(helpers, boss, 1)
                    helper_timer = 1 
        elif LEVEL == 6 : #Level 6 is a limitless level, just to increase the score after the boss,
                          #and uses all types of ennemeies (appart from the boss)
            if len(asteroids) <= 5 :
                asteroids = Asteroids.CreateNewAsteroids(asteroids)
            if len(spacedrones) <= 2 : 
                spacedrones = Space_Drones.CreateNewSpaceDrones(spacedrones)
            if len(fighters) <= 1 : 
                fighters = Alien_Fighters.CreateNewFighter(fighters)
            if score % 60  == 0 : 
                enemy_bullets = EnemyBullets.EnemiesShoot(fighters, mean_bullets)

        # Here comes the timer. It allows the player to keep shooting if they maintain the key pressed.
        if timer < 15 and timer > 0 : 
            timer += 1 
        elif timer >= 15 : 
            if score % 15 == 0 :  
                timer += 1 
                if len(bullets) <= add_new_bullet_rate : 
                    bullets = Bullets.CreateNewBullet(playerRect, bullets, False)

        if call_for_help :
            if helper_timer > 45 : 
                if score % 15 == 0 :
                    for a in helpers : 
                        rect = a['rect']
                        bullets = Bullets.CreateNewBullet(rect, bullets, True)
        
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
            if len(falcons) >= 1 : 
                falcons = millenium_falcon.MoveFalcon(falcons)
        elif LEVEL == 2 : 
            spacedrones = Space_Drones.MoveSpaceDronesToPlayer(playerRect, spacedrones)
        elif LEVEL == 3 : 
            fighters = Alien_Fighters.MoveFighter(fighters)
            enemy_bullets = EnemyBullets.MoveEnemyBullet(mean_bullets)
        elif LEVEL == 4 : 
            boss_facing = BossShip.CheckFacing(boss, boss_facing)
            for a in boss : 
                if a['rect'].y < y_final_pos :  
                    boss = BossShip.MoveBoss(boss)
                elif boss_facing == "left" : 
                    boss = BossShip.MoveBossLeft(boss)
                    helpers = Helpers.MoveHelpersLeft(helpers, boss)
                elif boss_facing == "right" : 
                    boss = BossShip.MoveBossRight(boss)
                    helpers = Helpers.MoveHelpersRight(helpers, boss)
            boss_bullets = BossBullets.MoveBossBullet(boss_bullets)
            boss_missiles = BossBombs.MoveBombsToPlayer(playerRect, boss_missiles)
            for a in helpers : 
                if a['rect'].y > WINDOWHEIGHT/2 + 100 : 
                    helpers = Helpers.MoveHelpers(helpers)
        elif LEVEL == 6 : 
            asteroids = Asteroids.MoveAsteroids(asteroids)
            spacedrones = Space_Drones.MoveSpaceDronesToPlayer(playerRect, spacedrones)
            fighters = Alien_Fighters.MoveFighter(fighters)
            enemy_bullets = EnemyBullets.MoveEnemyBullet(mean_bullets)
         
        # Now moving the bullets. Seperated because they will appear on every level.   
        bullets = Bullets.MoveBullet(bullets)

        # Delete ennemies that have fallen past the bottom.
        # Once again, checks the level.
        if LEVEL == 1 : 
            asteroids = Asteroids.DeleteAsteroids(asteroids)
            if len(falcons) >= 1 : 
                falcons = millenium_falcon.DeleteFalcon(falcons)
        elif LEVEL == 2 : 
            spacedrones = Space_Drones.DeleteSpaceDrones(spacedrones)
        elif LEVEL == 3 : 
            fighters = Alien_Fighters.DeleteFighter(fighters)
            mean_bullets  = EnemyBullets.DeleteEnemyBullet(mean_bullets)
        elif LEVEL == 4 : 
            boss = BossShip.DeleteBoss(boss)
            boss_bullets = BossBullets.DeleteBossBullet(boss_bullets)
            boss_missiles = BossBombs.DeleteBombs(boss_missiles)
            if helper_timer > 600 : 
                helpers = Helpers.DeleteHelpers(helpers)
                helper_timer = 0 
                helper_check = 1 
                call_for_help = False

        elif LEVEL == 6 :
            asteroids = Asteroids.DeleteAsteroids(asteroids) 
            spacedrones = Space_Drones.DeleteSpaceDrones(spacedrones)
            fighters = Alien_Fighters.DeleteFighter(fighters)
            mean_bullets  = EnemyBullets.DeleteEnemyBullet(mean_bullets)

        
        # Now deleting the bullets 
        bullets = Bullets.DeleteBullet(bullets)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        windowSurface.blit(backgroundImage, (0, 0))  # Draw the background image
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Level: %s' % (LEVEL), font, windowSurface, 10, 80) 

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each ennemy, according to the level.<
        if LEVEL == 0 : 
            draw_box_with_text(windowSurface, "Choose difficulty : Easy (1), Medium (2), Hard (3)", 0, WINDOWHEIGHT/3, WINDOWWIDTH, WINDOWHEIGHT/3, font_title)
        elif LEVEL == "To level 2" : 
            draw_box_with_text(windowSurface, 
                               "LEVEL 2 (RETURN)", 
                               0, WINDOWHEIGHT/2 - WINDOWHEIGHT/4, WINDOWWIDTH, WINDOWHEIGHT/3, font_title)
        elif LEVEL == "To level 3" : 
            draw_box_with_text(windowSurface, 
                               "LEVEL 3 (RETURN)", 
                               0, WINDOWHEIGHT/2 - WINDOWHEIGHT/4, WINDOWWIDTH, WINDOWHEIGHT/3, font_title)
        elif LEVEL == "To Boss" : 
            draw_box_with_text(windowSurface, 
                               "BOSS LEVEL (RETURN)", 
                               0, WINDOWHEIGHT/2 - WINDOWHEIGHT/4, WINDOWWIDTH, WINDOWHEIGHT/3, font_title)
        elif LEVEL == 1 or LEVEL == "PAUSE": 
            for a in asteroids : 
                windowSurface.blit(a['surface'], a['rect'])
            if len(falcons) >= 1 : 
                for a in falcons : 
                    windowSurface.blit(a['surface'], a['rect'])
        elif LEVEL == 2 or LEVEL == "PAUSE": 
            for a in spacedrones : 
                windowSurface.blit(a['surface'], a['rect'])
        elif LEVEL == 3 or LEVEL == "PAUSE": 
            for a in fighters :
                windowSurface.blit(a['surface'], a['rect'])
            for a in mean_bullets : 
                windowSurface.blit(a['surface'], a['rect'])
        elif LEVEL == 4 or LEVEL == "PAUSE": 
            for a in boss : 
                windowSurface.blit(a['surface'], a['rect'])
            for a in boss_bullets : 
                windowSurface.blit(a['surface'], a['rect'])
            for a in boss_missiles : 
                windowSurface.blit(a['surface'], a['rect'])
            for a in helpers : 
                windowSurface.blit(a['surface'], a['rect'])
            BossShip.DrawBossBar(windowSurface, boss, WINDOWWIDTH/2, 0)
            drawTitle("Alien Boss", font, windowSurface, WINDOWWIDTH/2, 20)
            drawText('Helpers Used : %s /1' % (helper_check), font, windowSurface, 10, 120)
        elif LEVEL == 5 : # This allows for the player to choose if he wants to stop or enter limitless mode.
            draw_box_with_text(windowSurface, 
                "Congrats, You've beaten the boss ! You can either stop now (ESC) or start our infinite mode to set a high score ! (RETURN)", 
                0, WINDOWHEIGHT/3, WINDOWWIDTH, WINDOWHEIGHT/3,font_title)
            limitless = True 
        elif LEVEL == 6 or LEVEL == "PAUSE": 
            for a in asteroids : 
                windowSurface.blit(a['surface'], a['rect'])
            for a in spacedrones : 
                windowSurface.blit(a['surface'], a['rect'])
            for a in fighters :
                windowSurface.blit(a['surface'], a['rect'])
            for a in mean_bullets : 
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
            if len(falcons) >= 1 : 
                if millenium_falcon.playerHasHitFlacon(playerRect, falcons) : 
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
            if EnemyBullets.playerHasHitBullet(playerRect, mean_bullets) : 
                if score > topScore : 
                    topScore = score 
                break
        elif LEVEL == 4 :
            if BossShip.playerHasHitBoss(playerRect, boss) : 
                if score > topScore : 
                    topScore = score 
                break 
            if BossBombs.playerHasHitBombs(playerRect, boss_missiles) : 
                if score > topScore : 
                    topScore = score 
                break
            if BossBullets.playerHasHitBossBullet(playerRect, boss_bullets) : 
                if score > topScore : 
                    topScore = score 
                break      
        elif LEVEL == 6 : 
            if Asteroids.playerHasHitAsteroids(playerRect, asteroids) : 
                if score > topScore : 
                    topScore = score 
                break
            if Space_Drones.playerHasHitSpaceDrone(playerRect, spacedrones) : 
                if score > topScore : 
                    topScore = score 
                break
            if Alien_Fighters.playerHasHitFighter(playerRect, fighters) :
                if score > topScore : 
                    topScore = score 
                break
            if EnemyBullets.playerHasHitBullet(playerRect, mean_bullets) :
                if score > topScore : 
                    topScore = score 
                break

        #Check if any bullets have hit the enemies.
        #Checking what ennemies to look in relation with the level 
        if LEVEL == 1 : 
            bullets, asteroids, score = Bullets.BulletHasHitAsteroids(bullets, asteroids, score, LEVEL)
            if len(falcons) >= 1 : 
                bullets, falcons, score = Bullets.BulletHasHitFalcon(bullets, falcons, score)
        elif LEVEL == 2 :               
            bullets, spacedrones, score = Bullets.BulletHasHitDrones(bullets, spacedrones, score, LEVEL)
        elif LEVEL == 3 :
            bullets, fighters, score = Bullets.BulletHasHitFighter(bullets, fighters, score, LEVEL)
        elif LEVEL == 4 :  
            bullets, boss, score, LEVEL, boss_dead = Bullets.BulletHasHitBoss(bullets, boss, score, LEVEL, boss_dead)
            bullets, boss_missiles = Bullets.BulletHasHitBomb(bullets, boss_missiles)
        elif LEVEL == 6 :
            bullets, asteroids, score = Bullets.BulletHasHitAsteroids(bullets, asteroids, score, LEVEL)
            bullets, spacedrones, score = Bullets.BulletHasHitDrones(bullets, spacedrones, score, LEVEL)
            bullets, fighters, score = Bullets.BulletHasHitFighter(bullets, fighters, score, LEVEL)

        


        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    #pygame.mixer.music.stop()
    volume = 0.2
    pygame.mixer.music.set_volume(volume)
    gameOverSound.play()

    drawTitle('GAME OVER', font_title, windowSurface, (WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))
    drawTitle('Press a key to play again.', font_title, windowSurface, (WINDOWWIDTH / 2), (WINDOWHEIGHT / 2) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
