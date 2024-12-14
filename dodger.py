import pygame, random, sys
from pygame.locals import *
from Asteroids_Class.Enemy_Class import *

# Defining all the important variables for later 
text_colour = (255, 255, 255)
background_colour = (255, 255, 255)
FPS = 60
player_move_rate = 5
add_new_bullet_rate = 5 
add_new_falcon_rate = 1
add_new_boss_rate = 1 
helpers_rate = 2
limitless_rate = 3
level = 0
facing = 1 
timer = 0 
helper_timer = 0 
helper_check = 0
limitless = False
call_for_help = False
AsteroidImage = pygame.image.load('Asteroids2.png')
pause = False
lvl = 0  
boss_facing = "left"
difficulty = 0 
boss_dead = False 
sound_played = False 

# Defining a few important functions 
def terminate():
    pygame.quit()
    sys.exit()

def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def draw_text(text, font, surface, x, y):
    textobj = font.render(text, 1, text_colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_title(text, font, surface, x, y):
    textobj1 = font.render(text, 1, text_colour)
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
window_width, window_height = screen_info.current_w, screen_info.current_h
window_surface = pygame.display.set_mode((window_width, window_height))

#Defines the name of the window 
pygame.display.set_caption('Galaxy Guardian')
pygame.mouse.set_visible(False)

# Set up the fonts.
font_path = 'Orbitron-Regular.ttf'  # Path to your custom font in the project folder
font = pygame.font.Font(font_path, 30)  # Load the custom font with a size of 48
font_title = pygame.font.Font(font_path, 50)

# Set up sounds.
pygame.mixer.init()
gameOverSound = pygame.mixer.Sound('laser.wav')
pygame.mixer.music.load('Asteroids_Music_final.wav')

# Set up images.
playerImage = pygame.image.load('Main_character_resized.png')
playerRect = playerImage.get_rect()
backgroundImage = pygame.image.load('space.jpg')  # Replace 'background.jpg' with your image file
backgroundImage = pygame.transform.scale(backgroundImage, (window_width, window_height))
logoImage = pygame.image.load("Logo2.png")
image_width, image_height = logoImage.get_size() # Calculate the position to center the image 
x_pos = (window_width - image_width) / 2 
y_pos = (window_height - image_height) / 2 - 100
Boss_image = pygame.image.load('Boss-ship.png')
Boss_width, Boss_height = Boss_image.get_size()
y_final_pos = -Boss_width/25 + 50


# Show the "Start" screen.
window_surface.blit(backgroundImage, (0, 0))  # Draw the image at the top-left corner of the screen
window_surface.blit(logoImage, (x_pos, y_pos ))
draw_title('Galaxy Guardian', font_title, window_surface, (window_width / 2), (window_height / 2))
draw_title('Press a key to start.', font, window_surface, (window_width // 2), (window_height // 2) + 50)
pygame.display.update()
wait_for_player_to_press_key()

topScore = 0
while True : 
    # Set up the start of the game.

    # Set up the lists of all ennemies 

    boss_dead = False 
    
    # Enemies of each level 
    asteroids = []
    spacedrones = []
    fighters = []
    falcons = []

    # The bullets (ours) and mean bullets (the ennemies)
    bullets = []
    mean_bullets = []
    
    # And everything regarding the boss. 
    # It gets it's own bullets because they have specific spawn points rather than the other bullets used by the ennemies. 
    # The bullets of the helpers are the same as we use, because we can just give their rect rather than ours. 
    boss = []
    helpers = []
    boss_bullets = []
    boss_missiles = []
    

    #Set up Score and Player 
    score = 0
    playerRect.topleft = (window_width / 2, window_height - 50)

    #Set up the movement and music 
    moveLeft = moveRight = moveUp = moveDown = False
    pygame.mixer.music.play(-1, 0.0)
    volume = 1
    pygame.mixer.music.set_volume(volume)

    #set up difficulty 

    while True: # The game loop runs while the game part is playing.

        # I will only increase the score while the game is playing. Like this, i can set up transition screens
        # between each levels and a pause button. 
        if not level == "To Boss" and not level == "To level 2" and not level == "To level 3" and not level == 5 and not level == "PAUSE" and not level == 0 : 
            score += 1  # Increase score.
        if not helper_timer == 0 : 
            helper_timer += 1 
        #Randomizes the chance to get the Easter Egg
        falcon_test = random.randint(1, 3000) 

        # The game defines on what level we are playing. 
        if pause : 
            # lvl variable is used to remember on which level we're playing. It is technically only necessary for when 
            # we are on the limitless level, that isn't defined by a score, but it is also a security to make sure 
            # no bugs can happen and we get teleported to another level. 
            lvl = level
            level = "PAUSE"
        elif score < 1500 and not level == 0 : 
            level = 1
        elif score > 1500 and score < 1510 : 
            level = "To level 2"
        elif score > 1510 and score < 4500 : 
           level = 2
           asteroids = [] #this is necessary because my pause level is made to display all ennemies, i therefore need to 
                          #empty the list
        elif score > 4500 and score < 4510 : 
            level = "To level 3"
        elif score > 4510 and score < 7500 : 
            level = 3
            spacedrones = []
        elif score > 7500 and score < 7510 : 
            level = "To Boss"
        elif score > 7510 and not level == 5 and not level == 6 and not level == "PAUSE" : 
            level = 4
            fighters = []
        elif score > 7510 and boss_dead and not level == 5 : 
            level = 6 

        # We now check for every action possible 

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                # We first check for actions moving the player, making sure he can't move if the game is on pause. 
                if event.key == K_LEFT or event.key == K_a :
                    if not level == "PAUSE" : 
                        moveRight = False
                        moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    if not level == "PAUSE" :
                        moveLeft = False
                        moveRight = True
                if event.key == K_UP or event.key == K_w:
                    if not level == "PAUSE" :
                        moveDown = False
                        moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    if not level == "PAUSE" :
                        moveUp = False
                        moveDown = True

                #We now check if the player wants to shoot. 
                if event.key == K_SPACE and not level == "PAUSE" : 
                    # Create a timer to able the player to keep shooting
                    timer = 1 
                    if len(bullets) <= add_new_bullet_rate : 
                        bullets = Bullets.CreateNewBullet(playerRect, bullets, False)

                #Here, we check if the player pressed a key to pass from a transition to the level. 
                if event.key == K_RETURN : 
                    if level == "To level 2" : 
                        level = 2 
                        score = 1510
                    elif level == "To level 3" : 
                        level = 3 
                        score = 4510
                    elif level == "To Boss" : 
                        level = 4
                        score = 7510
                
                    #I need to empty the remaining ennemies and bullets that may have stayed after the levels, so that when 
                    #we load the limitless level, we have an emtpy screen 
                    if limitless : 
                        level = 6
                        asteroids = []
                        spacedrones = []
                        fighters = []
                        mean_bullets = []
                
                #Check if the helpers have been activated. 
                if event.key == K_h : 
                    call_for_help = True 
                
                #We now check if the user wants to pause. We do not allow the player to pause the game during the boss level, because we felt like it would be better. 
                if event.key == K_LCTRL : 
                    if not level == 4 : 
                        if pause == True : 
                            pause = False
                            level = lvl
                        else : 
                            pause = True 
                
                #Level 0 is the choose difficulty screen. I set the difficulty value by checking what has been pressed. 
                if level == 0 : 
                    if event.key == K_1:  
                            difficulty = 1 
                            level = 1 
                    if event.key == K_2 :  
                            difficulty = 2
                            level = 1  
                    if event.key == K_3 : 
                            difficulty = 3
                            level = 1  

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
                if not level == "PAUSE" : 
                    playerRect.centerx = event.pos[0]
                    playerRect.centery = event.pos[1]
        
        #Now we apply the difficulty chosen on the first screen. It changes how many ennemies spawn on each level. 
        #The boss and the limitless level are unafected, by game design choice. 
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
        if level == 1 : 
            if len(asteroids) <= add_new_asteroid_rate :
                asteroids = Asteroids.CreateNewAsteroids(asteroids)
            if falcon_test == 9 and len(falcons) < add_new_falcon_rate : 
                falcons = millenium_falcon.CreateNewFalcon(falcons)
        elif level == 2 : 
            if len(spacedrones) <= add_new_spacedrone_rate : 
                spacedrones = Space_Drones.CreateNewSpaceDrones(spacedrones)
        elif level == 3 : 
            if len(fighters) <= add_new_fighter_rate : 
                fighters = Alien_Fighters.CreateNewFighter(fighters)
            if score % 60  == 0 : #This makes the ennemies shoot only once every second (game playing at 60 FPS, and score += 1 every frame)
                enemy_bullets = EnemyBullets.EnemiesShoot(fighters, mean_bullets)
        elif level == 4 : 
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
        elif level == 6 : #Level 6 is a limitless level, just to increase the score after the boss,
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
        # This first condition is needed because by pressing the button, the player shoots, and then if the key is maintained, 
        # it shot a second bullet on the same frame (or on the frame after) which created some problems. 
        if timer < 15 and timer > 0 : 
            timer += 1 
        elif timer >= 15 : 
            if score % 15 == 0 :  
                timer += 1 
                if len(bullets) <= add_new_bullet_rate : 
                    bullets = Bullets.CreateNewBullet(playerRect, bullets, False)

        # Here we make the helpers shoot at the same rate as the player. 
        # The timer is here to make it so that they don't shoot before they arrive at their final height.
        if call_for_help :
            if helper_timer > 45 : 
                if score % 15 == 0 :
                    for a in helpers : 
                        rect = a['rect']
                        bullets = Bullets.CreateNewBullet(rect, bullets, True)
        
        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * player_move_rate, 0)
        if moveRight and playerRect.right < window_width:
            playerRect.move_ip(player_move_rate, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * player_move_rate)
        if moveDown and playerRect.bottom < window_height:
            playerRect.move_ip(0, player_move_rate)

        # Move the enemies down.
        # It checks what enemies to move according to the level. 
        if level == 1 : 
            asteroids = Asteroids.MoveAsteroids(asteroids)
            if len(falcons) >= 1 : 
                falcons = millenium_falcon.MoveFalcon(falcons)
        elif level == 2 : 
            spacedrones = Space_Drones.MoveSpaceDronesToPlayer(playerRect, spacedrones)
        elif level == 3 : 
            fighters = Alien_Fighters.MoveFighter(fighters)
            enemy_bullets = EnemyBullets.MoveEnemyBullet(mean_bullets)
        elif level == 4 : 
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
                if a['rect'].y > window_height/2 + 100 : 
                    helpers = Helpers.MoveHelpers(helpers)
        elif level == 6 : 
            asteroids = Asteroids.MoveAsteroids(asteroids)
            spacedrones = Space_Drones.MoveSpaceDronesToPlayer(playerRect, spacedrones)
            fighters = Alien_Fighters.MoveFighter(fighters)
            enemy_bullets = EnemyBullets.MoveEnemyBullet(mean_bullets)
         
        # Now moving the bullets. Seperated because they will appear on every level.   
        bullets = Bullets.MoveBullet(bullets)

        # Delete ennemies that have fallen past the bottom.
        # Once again, checks the level.
        if level == 1 : 
            asteroids = Asteroids.DeleteAsteroids(asteroids)
            if len(falcons) >= 1 : 
                falcons = millenium_falcon.DeleteFalcon(falcons)
        elif level == 2 : 
            spacedrones = Space_Drones.DeleteSpaceDrones(spacedrones)
        elif level == 3 : 
            fighters = Alien_Fighters.DeleteFighter(fighters)
            mean_bullets  = EnemyBullets.DeleteEnemyBullet(mean_bullets)
        elif level == 4 : 
            boss = BossShip.DeleteBoss(boss)
            boss_bullets = BossBullets.DeleteBossBullet(boss_bullets)
            boss_missiles = BossBombs.DeleteBombs(boss_missiles)
            # The helpers never die of getting to the bottom of the screen, so we use this fonction to kill them 
            # when it's been long enough (here 10 seconds)
            if helper_timer > 600 : 
                helpers = Helpers.DeleteHelpers(helpers)
                helper_timer = 0 
                helper_check = 1 
                call_for_help = False

        elif level == 6 :
            asteroids = Asteroids.DeleteAsteroids(asteroids) 
            spacedrones = Space_Drones.DeleteSpaceDrones(spacedrones)
            fighters = Alien_Fighters.DeleteFighter(fighters)
            mean_bullets  = EnemyBullets.DeleteEnemyBullet(mean_bullets)

        
        # Now deleting the bullets 
        bullets = Bullets.DeleteBullet(bullets)

        # Draw the game world on the window.
        window_surface.fill(background_colour)

        # Draw the score and top score.
        window_surface.blit(backgroundImage, (0, 0))  # Draw the background image
        draw_text('Score: %s' % (score), font, window_surface, 10, 0)
        draw_text('Top Score: %s' % (topScore), font, window_surface, 10, 40)
        draw_text('Level: %s' % (level), font, window_surface, 10, 80) 

        # Draw the player's rectangle.
        window_surface.blit(playerImage, playerRect)

        # Here we draw every box that sits in transition phases. 
        if level == 0 : 
            draw_box_with_text(window_surface, "Choose difficulty : Easy (1), Medium (2), Hard (3)", 0, window_height/3, window_width, window_height/3, font_title)
        elif level == "To level 2" : 
            draw_box_with_text(window_surface, 
                               "LEVEL 2 (RETURN)", 
                               0, window_height/2 - window_height/4, window_width, window_height/3, font_title)
        elif level == "To level 3" : 
            draw_box_with_text(window_surface, 
                               "LEVEL 3 (RETURN)", 
                               0, window_height/2 - window_height/4, window_width, window_height/3, font_title)
        elif level == "To Boss" : 
            draw_box_with_text(window_surface, 
                               "BOSS LEVEL (RETURN)", 
                               0, window_height/2 - window_height/4, window_width, window_height/3, font_title)
        elif level == 5 : # This allows for the player to choose if he wants to stop or enter limitless mode once 
                          # The boss has been beaten.
            draw_box_with_text(window_surface, 
                "Congrats, You've beaten the boss ! You can either stop now (ESC) or start our infinite mode to set a high score ! (RETURN)", 
                0, window_height/3, window_width, window_height/3,font_title)
            limitless = True 
            
        # We here then draw all of the ennemies according to their levels. 
        elif level == 1 :
            for a in asteroids : 
                window_surface.blit(a['surface'], a['rect'])
            if len(falcons) >= 1 : 
                for a in falcons : 
                    window_surface.blit(a['surface'], a['rect'])
        elif level == 2 :
            for a in spacedrones : 
                window_surface.blit(a['surface'], a['rect'])
        elif level == 3 : 
            for a in fighters :
                window_surface.blit(a['surface'], a['rect'])
            for a in mean_bullets : 
                window_surface.blit(a['surface'], a['rect'])
        elif level == 4 :
            for a in boss : 
                window_surface.blit(a['surface'], a['rect'])
            for a in boss_bullets : 
                window_surface.blit(a['surface'], a['rect'])
            for a in boss_missiles : 
                window_surface.blit(a['surface'], a['rect'])
            for a in helpers : 
                window_surface.blit(a['surface'], a['rect'])
            # We here draw a boss bar. 
            BossShip.DrawBossBar(window_surface, boss, window_width/2, 0)
            draw_title("Alien Boss", font, window_surface, window_width/2, 20)
            draw_text('Helpers Used : %s /1' % (helper_check), font, window_surface, 10, 120)
        elif level == 6 or level == "PAUSE": 
            for a in asteroids : 
                window_surface.blit(a['surface'], a['rect'])
            for a in spacedrones : 
                window_surface.blit(a['surface'], a['rect'])
            for a in fighters :
                window_surface.blit(a['surface'], a['rect'])
            for a in mean_bullets : 
                window_surface.blit(a['surface'], a['rect'])
            
        # Drawing the Bullets. This is out of the conditions because it will happen at every single level. 
        for a in bullets : 
            window_surface.blit(a['surface'], a['rect'])

        pygame.display.update()

        # Check if any of the ennemies have hit the player.
        if level == 1 : 
            if Asteroids.playerHasHitAsteroids(playerRect, asteroids) : 
                if score > topScore : 
                    topScore = score 
                break
            if len(falcons) >= 1 : 
                if millenium_falcon.playerHasHitFlacon(playerRect, falcons) : 
                    if score > topScore : 
                        topScore = score 
                    break
        elif level == 2 : 
            if Space_Drones.playerHasHitSpaceDrone(playerRect, spacedrones) : 
                if score > topScore : 
                    topScore = score 
                break 
        elif level == 3 : 
            if Alien_Fighters.playerHasHitFighter(playerRect, fighters) : 
                if score > topScore : 
                    topScore = score 
                break 
            if EnemyBullets.playerHasHitBullet(playerRect, mean_bullets) : 
                if score > topScore : 
                    topScore = score 
                break
        elif level == 4 :
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
        elif level == 6 : 
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
        if level == 1 : 
            bullets, asteroids, score = Bullets.BulletHasHitAsteroids(bullets, asteroids, score, level)
            if len(falcons) >= 1 : 
                bullets, falcons, score = Bullets.BulletHasHitFalcon(bullets, falcons, score)
        elif level == 2 :               
            bullets, spacedrones, score = Bullets.BulletHasHitDrones(bullets, spacedrones, score, level)
        elif level == 3 :
            bullets, fighters, score = Bullets.BulletHasHitFighter(bullets, fighters, score, level)
        elif level == 4 :  
            bullets, boss, score, level, boss_dead = Bullets.BulletHasHitBoss(bullets, boss, score, level, boss_dead)
            bullets, boss_missiles = Bullets.BulletHasHitBomb(bullets, boss_missiles)
        elif level == 6 :
            bullets, asteroids, score = Bullets.BulletHasHitAsteroids(bullets, asteroids, score, level)
            bullets, spacedrones, score = Bullets.BulletHasHitDrones(bullets, spacedrones, score, level)
            bullets, fighters, score = Bullets.BulletHasHitFighter(bullets, fighters, score, level)

        

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    #pygame.mixer.music.stop()
    volume = 0.2
    pygame.mixer.music.set_volume(volume)
    gameOverSound.play()

    draw_title('GAME OVER', font_title, window_surface, (window_width / 2), (window_height / 2))
    draw_title('Press a key to play again.', font_title, window_surface, (window_width / 2), (window_height / 2) + 50)
    pygame.display.update()
    wait_for_player_to_press_key()

    gameOverSound.stop()
