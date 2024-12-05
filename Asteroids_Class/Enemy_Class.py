import pygame, random, sys
from pygame.locals import *

#Checking the screen size to adapt the spawning of the different ennemies 
pygame.init()
screen_info = pygame.display.Info() 
WINDOWWIDTH, WINDOWHEIGHT = int(screen_info.current_w), int(screen_info.current_h)

# Loading all od the images 
AsteroidImage = pygame.image.load('Asteroids2.png')
AsteroidImageRight = pygame.image.load('Asteroids2_right.png')
AsteroidImageLeft = pygame.image.load('Asteroids2_left.png')
SpaceDroneImage = pygame.image.load('Space_Drones.png')
AlienFighterImage = pygame.image.load('ALien_Fighter.png')
BossShipImage = pygame.image.load('Boss-ship.png')
BulletImage = pygame.image.load('laser_bullets.png')
HelperBulletImage = pygame.image.load('laser_bullets_helpers.png')
EnemyBulletImage = pygame.image.load('laser_bullets_enemy.png')
FalconImage = pygame.image.load('falcon.png')
MissileImage = pygame.image.load('missile.png')
HelperImage = pygame.image.load('helper.png')
facing = "left"

# The structure of each ennemy is the same ish. We have methods to create, move, 
# destroy if it touches the bottom, and check if it got shot. 
# However, they all have specificities that I'll be commenting on. 

class Asteroids : 
    asteroids_min_size = 20
    asteroids_max_size = 80
    asteroids_min_speed = 2  
    asteroids_max_speed = 8

    def CreateNewAsteroids(a_list) : 
        asteroids_size = random.randint(Asteroids.asteroids_min_size, Asteroids.asteroids_max_size)
        newAsteroid = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - asteroids_size), 0 - asteroids_size, asteroids_size, asteroids_size), 'speed': random.randint(Asteroids.asteroids_min_speed, Asteroids.asteroids_max_speed), 'surface':pygame.transform.scale(AsteroidImage, (asteroids_size, asteroids_size)), 'behaviour' : random.randint(1,5)}
        
        # This makes so that the asteroids can go diagonal, and that their image will switch directions accordingly
        if newAsteroid['behaviour'] == 5 : 
            if newAsteroid['rect'].x > WINDOWWIDTH/2 : 
                newAsteroid['facing'] = "left"
                newAsteroid['surface'] = pygame.transform.scale(AsteroidImageLeft, (asteroids_size, asteroids_size))
            elif newAsteroid['rect'].x < WINDOWWIDTH/2 : 
                newAsteroid['facing'] = "right"
                newAsteroid['surface'] = pygame.transform.scale(AsteroidImageRight, (asteroids_size, asteroids_size))
            elif newAsteroid['rect'] == WINDOWWIDTH/2 : 
                pass
        a_list.append(newAsteroid)
        return a_list

    def MoveAsteroids (a_list2) :
        for a in a_list2:
            if a['behaviour'] < 5 : 
                a['rect'].move_ip(0, a['speed'])
            elif a['behaviour'] == 5 and a['facing'] == "right":
                a['rect'].move_ip(a['speed']/2, a['speed'])
            elif a['behaviour'] == 5 and a['facing'] == "left" :
                a['rect'].move_ip(-a['speed'], a['speed'])
        return a_list2
    
    def DeleteAsteroids(asteroids_list2) :
        for a in asteroids_list2[:] :
            if a['rect'].top > WINDOWHEIGHT:
                asteroids_list2.remove(a)
        return asteroids_list2
    

    def playerHasHitAsteroids(playerRect, asteroids):
        for a in asteroids:
            if playerRect.colliderect(a['rect']):
                return True
        return False
    
# Our easter egg. It appears (on average) once every 2 games. 
# It can only appear in the 1st Level, and only 1 by game. 
# When destroyed, it will bump the score enough to go directly to Level 3. 
class millenium_falcon : 
    falcon_size = 50
    falcon_speed = 2  

    def CreateNewFalcon(a_list) : 
        Falcon_size = millenium_falcon.falcon_size
        Falcon_speed = millenium_falcon.falcon_speed
        newFalcon = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - Falcon_size), 0 - Falcon_size, Falcon_size, Falcon_size), 'speed': Falcon_speed, 'surface':pygame.transform.scale(FalconImage, (Falcon_size, 2.2 * Falcon_size)),}
        a_list.append(newFalcon)
        return a_list

    def MoveFalcon (a_list2) :
        for a in a_list2: 
            a['rect'].move_ip(0, a['speed'])
        return a_list2
    
    def DeleteFalcon(asteroids_list2) :
        for a in asteroids_list2[:] :
            if a['rect'].top > WINDOWHEIGHT:
                asteroids_list2.remove(a)
        return asteroids_list2

    def playerHasHitFlacon(playerRect, asteroids):
        for a in asteroids:
            if playerRect.colliderect(a['rect']):
                return True
        return False

class Space_Drones : 
    space_drones_min_size = 30
    space_drones_max_size = 80 
    space_drones_min_speed = 2 
    space_drones_max_speed = 10
    space_drones_min_hor_speed = 1
    space_drones_max_hor_speed = 4

    def CreateNewSpaceDrones(a_list) : 
        SpaceDrones_size = random.randint(Space_Drones.space_drones_min_size, Space_Drones.space_drones_max_size)
        newSpaceDrone = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - SpaceDrones_size), 0 - SpaceDrones_size, SpaceDrones_size, SpaceDrones_size), 'speed': random.randint(Space_Drones.space_drones_min_speed, Space_Drones.space_drones_max_speed), 'horizontal_speed' : random.randint(Space_Drones.space_drones_min_hor_speed, Space_Drones.space_drones_max_hor_speed), 'surface':pygame.transform.scale(SpaceDroneImage, (SpaceDrones_size, SpaceDrones_size)),}
        a_list.append(newSpaceDrone)
        return a_list
    
    # This function allows our Level 2 Ennemies to be "intelligent" (AKA, they try to reach the player)
    def MoveSpaceDronesToPlayer (playerRect, a_list2) : 
        for a in a_list2 : 
            if playerRect.centerx > a['rect'].x : 
                a['rect'].move_ip(a['horizontal_speed'], a['speed'])
            elif playerRect.centerx < a['rect'].x : 
                a['rect'].move_ip(-a['horizontal_speed'], a['speed'])
            elif playerRect.centerx == a['rect'].x : 
                a['rect'].move_ip(0, a['speed'])
        return a_list2

    def DeleteSpaceDrones(spacedrones_list2) :
        for a in spacedrones_list2[:] :
            if a['rect'].top > WINDOWHEIGHT:
                spacedrones_list2.remove(a)
        return spacedrones_list2
    
    def playerHasHitSpaceDrone(playerRect, spacedrones):
        for a in spacedrones:
            if playerRect.colliderect(a['rect']):
                return True
        return False


class Alien_Fighters : 
    fighters_min_size = 30
    fighters_max_size = 90
    fighters_min_speed = 3
    fighters_max_speed = 10

    def CreateNewFighter(a_list) : 
        Fighter_size = random.randint(Alien_Fighters.fighters_min_size, Alien_Fighters.fighters_max_size)
        newFighter = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - Fighter_size), 0 - Fighter_size, Fighter_size, Fighter_size), 'speed': random.randint(Alien_Fighters.fighters_min_speed, Alien_Fighters.fighters_max_speed), 'surface':pygame.transform.scale(AlienFighterImage, (Fighter_size, Fighter_size)),}
        if newFighter['rect'].x > WINDOWWIDTH/2 : 
                newFighter['facing'] = "left"
        elif newFighter['rect'].x < WINDOWWIDTH/2 : 
                newFighter['facing'] = "right"
        elif newFighter['rect'] == WINDOWWIDTH/2 : 
                newFighter['facing'] = "right"
        a_list.append(newFighter)
        return a_list
    
    # Our Level 3 ennemies, like the asteroids, need a "facing". This will allow them to go in the opposite side 
    # of the screen, rather than going diagonal in the same direction they are, which makes them disappear too fast. 
    def MoveFighter (a_list2) :
        for a in a_list2:
            if a['facing'] == "right":
                a['rect'].move_ip(a['speed']/2, a['speed'])
            if a['facing'] == "left" : 
                a['rect'].move_ip(-a['speed']/2, a['speed'])
        return a_list2
    
    def DeleteFighter(fighters_list2) :
        for a in fighters_list2[:] :
            if a['rect'].top > WINDOWHEIGHT:
                fighters_list2.remove(a)
        return fighters_list2
    
    def playerHasHitFighter(playerRect, fighters):
        for a in fighters:
            if playerRect.colliderect(a['rect']):
                return True
        return False
    

# Our Boss class. It can be created (only 1), moved, destroyed if it reaches the bottom. 
# It has a "LIFE" parameter. It is it's health points. The amount of bullets needed to take it down. 
class BossShip() : 
    boss_ship_size = 500
    boss_ship_speed = 10
    image_width, image_height = BossShipImage.get_size() # Calculate the position to center the image 
    x_pos = (WINDOWWIDTH - image_width)/2
    y_pos = -image_height
    y_final_pos = -image_height/18
    boss_health = 200

    def CreateNewBoss(a_list) : 
        Ship_size_x = BossShip.image_width 
        Ship_size_y = BossShip.image_height 
        Ship_Speed = BossShip.boss_ship_speed
        x_posi = BossShip.x_pos
        y_posi = BossShip.y_pos
        boss_life = BossShip.boss_health
        newBoss = {'rect': pygame.Rect(x_posi, y_posi, Ship_size_x, Ship_size_y), 'speed': Ship_Speed, 'surface':pygame.transform.scale(BossShipImage, (Ship_size_x, Ship_size_y)), 'life' : boss_life,}
        a_list.append(newBoss)
        print(BossShip.image_width)
        print(WINDOWWIDTH)
        return a_list
    
    def MoveBoss (a_list2) :
        for a in a_list2:
            a['rect'].move_ip(0, a['speed'])
        return a_list2
    
    def DeleteBoss(list_2) :
        for a in list_2[:] :
            if a['rect'].top > WINDOWHEIGHT:
                list_2.remove(a)
        return list_2
    
    def playerHasHitBoss(playerRect, boss):
        for a in boss:
            if playerRect.colliderect(a['rect']):
                return True
        return False
    
    def DrawBossBar(screen, list, x, y) :
        current_bar_width =  list[0]['life']*2
        bar_height = 40
        bar_width = BossShip.boss_health*2
        x_pos = x - bar_width/2
        pygame.draw.rect(screen, (255,0,0), (x_pos, y, current_bar_width, bar_height)) 
        # Draw the bar outline 
        pygame.draw.rect(screen, (255,255,255), (x_pos, y, bar_width, bar_height), 2)
    
class Helpers() : 
    helpers_size = 50
    helpers_speed = -4 
    x_spawn = [WINDOWWIDTH/2 - 100, WINDOWWIDTH/2 + 100]

    def CallForHelpers(a_list, facing) : 
        Size = Helpers.helpers_size
        Speed = Helpers.helpers_speed 
        x_pos = Helpers.x_spawn[facing]
        newHelper =  {'rect': pygame.Rect(x_pos, WINDOWHEIGHT, Size, Size), 'speed': Speed, 'surface':pygame.transform.scale(HelperImage, (Size, Size))}
        a_list.append(newHelper)
        return a_list 
    
    def MoveHelpers(a_list) : 
        for a in a_list : 
            a['rect'].move_ip(0, a['speed'])
        return a_list
    
    def DeleteHelpers(a_list) : 
        a_list = []
        return a_list
    

# The player bullets. They have methods to create, move, delete if it's too high, and one method for each ennemy 
# to check if it was hit by it.     
class Bullets : 
    bullet_size = 30
    bullet_speed = -10

    def CreateNewBullet(playerRect, a_list, boolean) : 
        Bullet_size = Bullets.bullet_size
        Bullet_speed = Bullets.bullet_speed
        newBullet = {'rect': pygame.Rect(playerRect.centerx - 15, (playerRect.centery - 30), Bullet_size, Bullet_size), 'speed': Bullet_speed, 'surface':pygame.transform.scale(BulletImage, (Bullet_size, Bullet_size)),}
        if boolean : 
            newBullet['surface'] = pygame.transform.scale(HelperBulletImage, (Bullet_size, Bullet_size))
        a_list.append(newBullet)
        return a_list
    
    def MoveBullet (a_list2) :
        for a in a_list2 : 
            a['rect'].move_ip(0, a['speed'])
        return a_list2
    
    def DeleteBullet(bullet_list2) :
        for a in bullet_list2[:] :
            if a['rect'].bottom < 0 :
                bullet_list2.remove(a)
        return bullet_list2


    
    def BulletHasHitAsteroids(bullets, asteroids, score) :
        for a in asteroids :
            for b in bullets : 
                if b['rect'].colliderect(a['rect']):
                    asteroids.remove(a)
                    bullets.remove(b)
                    score += 50
                    if score > 1500 : 
                        score = 1501
        return bullets, asteroids, score
    

    def BulletHasHitDrones(bullets, spacedrones, score) : 
        for a in spacedrones :
            for b in bullets : 
                if b['rect'].colliderect(a['rect']):
                    spacedrones.remove(a)
                    bullets.remove(b)
                    score += 100
                    if score > 4500 : 
                        score = 4500
        return bullets, spacedrones, score 

    def BulletHasHitFighter(bullets, fighters, score):
        for a in fighters :
            for b in bullets : 
                if b['rect'].colliderect(a['rect']):
                    fighters.remove(a)
                    bullets.remove(b)
                    score += 200
                    if score > 7500 : 
                        score = 4500
        return bullets, fighters, score
    
    def BulletHasHitFalcon(bullets, fighters, score):
        for a in fighters :
            for b in bullets : 
                if b['rect'].colliderect(a['rect']):
                    fighters.remove(a)
                    bullets.remove(b)
                    score = 5000
        return bullets, fighters, score
    
    def BulletHasHitBoss(bullets, boss, score, LEVEL):
        for a in boss :
            for b in bullets : 
                if b['rect'].colliderect(a['rect']):
                    if a['life'] > 1 : 
                        a['life'] -= 1 
                        bullets.remove(b)
                    elif a['life'] == 1 : 
                        boss.remove(a)
                        bullets.remove(b)
                        LEVEL = 5
                        score += 3000
        return bullets, boss, score, LEVEL
    
    def BulletHasHitBomb(bullets, boss_missiles,):
        for a in boss_missiles :
            for b in bullets : 
                if b['rect'].colliderect(a['rect']):
                    boss_missiles.remove(a)
                    bullets.remove(b)
        return bullets, boss_missiles

# The bullets that the Level 3 Ennemies can shoot. They behave the same way as a normal ennemy,
# appart from their spawn place, as they spawn just under the ennemy "shooting" it. 
# They cannot be destroyed by the player's bullets. 
class EnemyBullets : 
    bullet_size = 30
    bullet_speed = 10

    def EnemiesShoot(enemy_list, a_list) : 
        for a in enemy_list : 
            Bullet_size = EnemyBullets.bullet_size
            Bullet_speed = EnemyBullets.bullet_speed
            newBullet = {'rect': pygame.Rect(a['rect'].x + 20, a['rect'].y + 40, Bullet_size, Bullet_size), 'speed': Bullet_speed, 'surface':pygame.transform.scale(EnemyBulletImage, (Bullet_size, Bullet_size)),}
            a_list.append(newBullet)
        return a_list
    
    def MoveEnemyBullet (a_list2) :
        for a in a_list2 : 
            a['rect'].move_ip(0, a['speed'])
        return a_list2
    
    def DeleteEnemyBullet(bullet_list2) :
        for a in bullet_list2[:] :
            if a['rect'].bottom < 0 :
                bullet_list2.remove(a)
        return bullet_list2
    
    def playerHasHitBullet(playerRect, enemy_bullet):
        for a in enemy_bullet:
            if playerRect.colliderect(a['rect']):
                return True
        return False
    
# The bullets that the boss can shoot. I thought about using the classic "ennemy bullets", but seeing as they are 
# limited to one spawn point, i added this new class. 
# They are shot from 6 different places from the boss, detailed in x_spawn.    
# They cannot be destroyed by the player's bullets
class BossBullets : 
    bullet_size = 30
    bullet_speed = 10
    image_width, image_height = BossShipImage.get_size() # Calculate the position to center the image 
    y_pos = image_height/2 + 70
    x_pos = (WINDOWWIDTH - image_width)/2
    x_spawn = [x_pos + 60, x_pos + 120, x_pos + 180, WINDOWWIDTH - x_pos - 60, WINDOWWIDTH - x_pos - 120, WINDOWWIDTH - x_pos - 180 ]
    y_spawn = y_pos

    def BossShoot(a_list) : 
        for a in BossBullets.x_spawn : 
            Bullet_size = BossBullets.bullet_size
            Bullet_speed = BossBullets.bullet_speed
            newBullet = {'rect': pygame.Rect(a, BossBullets.y_spawn, Bullet_size, Bullet_size), 'speed': Bullet_speed, 'surface':pygame.transform.scale(EnemyBulletImage, (Bullet_size, Bullet_size)),}
            a_list.append(newBullet)
        return a_list
    
    def MoveBossBullet (a_list2) :
        for a in a_list2:
            a['rect'].move_ip(0, a['speed'])
        return a_list2
    
    def DeleteBossBullet(bullet_list2) :
        for a in bullet_list2[:] :
            if a['rect'].bottom < 0 :
                bullet_list2.remove(a)
        return bullet_list2
    
    def playerHasHitBossBullet(playerRect, enemy_bullet):
        for a in enemy_bullet:
            if playerRect.colliderect(a['rect']):
                return True
        return False

# These bombs are shot by the boss. 
# They are chasing the player to make the boss harder. 
# They can spawn from two different points on the boss, detailed in x_spawn. 
# When created, they need a "facing" to tell them on which side they get shot from. 
# I did it this way to be able to alternate the spawn points in the main loop.
# They can be destroyed by the players bullets. 
class BossBombs : 
    bomb_size = 50
    bomb_speed = 2
    image_width, image_height = BossShipImage.get_size() # Calculate the position to center the image 
    y_pos = image_height/2 + 70
    x_pos = (WINDOWWIDTH - image_width)/2
    x_spawn = [x_pos + 250, WINDOWWIDTH - x_pos - 250 ]
    y_spawn = y_pos
    bomb_width, bomb_height = MissileImage.get_size()


    def BossShootsBombs(a_list, facing) : 
        for a in BossBombs.x_spawn : 
            Bomb_width = BossBombs.bomb_width/10
            Bomb_height = BossBombs.bomb_height/10
            Bomb_speed = BossBombs.bomb_speed
            if facing == 1 : 
                X_spawn = BossBombs.x_spawn[0] 
            elif facing == 2 : 
                X_spawn = BossBombs.x_spawn[1]
            newBomb = {'rect': pygame.Rect(X_spawn, BossBombs.y_spawn, Bomb_width, Bomb_height), 'speed': Bomb_speed, 'surface':pygame.transform.scale(MissileImage, (Bomb_width, Bomb_height)),}
            a_list.append(newBomb)
        return a_list

    def MoveBombsToPlayer (playerRect, a_list2) : 
        for a in a_list2 : 
            if playerRect.centerx > a['rect'].x : 
                a['rect'].move_ip(a['speed'], a['speed'])
            elif playerRect.centerx < a['rect'].x : 
                a['rect'].move_ip(-a['speed'], a['speed'])
            elif playerRect.centerx == a['rect'].x : 
                a['rect'].move_ip(0, a['speed'])
        return a_list2

    
    def DeleteBombs(bombs_list2) :
        for a in bombs_list2[:] :
            if a['rect'].top > WINDOWHEIGHT:
                bombs_list2.remove(a)
        return bombs_list2
    
    def playerHasHitBombs(playerRect, bombs):
        for a in bombs:
            if playerRect.colliderect(a['rect']):
                return True
        return False