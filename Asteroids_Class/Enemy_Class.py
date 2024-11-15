import pygame, random, sys
from pygame.locals import *

pygame.init()
screen_info = pygame.display.Info() 
WINDOWWIDTH, WINDOWHEIGHT = int(screen_info.current_w), int(screen_info.current_h)

AsteroidImage = pygame.image.load('Asteroids2.png')
AsteroidImageRight = pygame.image.load('Asteroids2_right.png')
AsteroidImageLeft = pygame.image.load('Asteroids2_left.png')
SpaceDroneImage = pygame.image.load('Space_Drones.png')
AlienFighterImage = pygame.image.load('ALien_Fighter.png')
BossShipImage = pygame.image.load('Boss-ship.png')
BulletImage = pygame.image.load('laser_bullets.png')
reverseCheat = slowCheat = False

class Asteroids : 
    asteroids_min_size = 20
    asteroids_max_size = 80
    asteroids_min_speed = 2  
    asteroids_max_speed = 8

    def CreateNewAsteroids(a_list) : 
        asteroids_size = random.randint(Asteroids.asteroids_min_size, Asteroids.asteroids_max_size)
        newAsteroid = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - asteroids_size), 0 - asteroids_size, asteroids_size, asteroids_size), 'speed': random.randint(Asteroids.asteroids_min_speed, Asteroids.asteroids_max_speed), 'surface':pygame.transform.scale(AsteroidImage, (asteroids_size, asteroids_size)), 'behaviour' : random.randint(1,5)}
        if newAsteroid['behaviour'] == 5 : 
            if newAsteroid['rect'].x > WINDOWWIDTH/2 : 
                newAsteroid['facing'] = "left"
                newAsteroid['surface'] = pygame.transform.scale(AsteroidImageLeft, (asteroids_size, asteroids_size))
            elif newAsteroid['rect'].x < WINDOWWIDTH/2 : 
                newAsteroid['facing'] = "right"
                newAsteroid['surface'] = pygame.transform.scale(AsteroidImageRight, (asteroids_size, asteroids_size))
            elif newAsteroid['rect'] == WINDOWWIDTH/2 : 
                pass
        print(newAsteroid)
        a_list.append(newAsteroid)
        return a_list

    def MoveAsteroids (a_list2) :
        for a in a_list2:
            if a['behaviour'] < 5 : 
                if not reverseCheat and not slowCheat:
                    a['rect'].move_ip(0, a['speed'])
                elif reverseCheat:
                    a['rect'].move_ip(0, -5)
                elif slowCheat:
                    a['rect'].move_ip(0, 1)
            elif a['behaviour'] == 5 and a['facing'] == "right":
                if not reverseCheat and not slowCheat:
                    a['rect'].move_ip(a['speed']/2, a['speed'])
            elif a['behaviour'] == 5 and a['facing'] == "left" :
                if not reverseCheat and not slowCheat : 
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
        print(newSpaceDrone)
        a_list.append(newSpaceDrone)
        return a_list
    
    def MoveSpaceDrones (a_list2) :
        for a in a_list2:
            if not reverseCheat and not slowCheat:
                a['rect'].move_ip(0, a['speed'])
            elif reverseCheat:
                a['rect'].move_ip(0, -5)
            elif slowCheat:
                a['rect'].move_ip(0, 1)
        return a_list2
    
    def MoveSpaceDronesToPlayer (playerRect, a_list2) : 
        for a in a_list2 : 
            if playerRect.centerx > a['rect'].x : 
                a['rect'].move_ip(a['horizontal_speed'], a['speed'])
            elif playerRect.centerx < a['rect'].x : 
                a['rect'].move_ip(-a['horizontal_speed'], a['speed'])
            elif playerRect.centerx == a['rect'].x : 
                pass
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
    fighters_min_speed = 5
    fighters_max_speed = 15

    def CreateNewFighter(a_list) : 
        Fighter_size = random.randint(Alien_Fighters.fighters_min_size, Alien_Fighters.fighters_max_size)
        newFighter = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - Fighter_size), 0 - Fighter_size, Fighter_size, Fighter_size), 'speed': random.randint(Alien_Fighters.fighters_min_speed, Alien_Fighters.fighters_max_speed), 'surface':pygame.transform.scale(AlienFighterImage, (Fighter_size, Fighter_size)),}
        print(newFighter)
        a_list.append(newFighter)
        return a_list
    
    def MoveFighter (a_list2) :
        for a in a_list2:
            if not reverseCheat and not slowCheat:
                a['rect'].move_ip(0, a['speed'])
            elif reverseCheat:
                a['rect'].move_ip(0, -5)
            elif slowCheat:
                a['rect'].move_ip(0, 1)
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
    
class Bullets : 
    bullet_size = 30
    bullet_speed = -10

    def CreateNewBullet(playerRect, a_list) : 
        Bullet_size = Bullets.bullet_size
        Bullet_speed = Bullets.bullet_speed
        newBullet = {'rect': pygame.Rect(playerRect.centerx - 15, (playerRect.centery - 30), Bullet_size, Bullet_size), 'speed': Bullet_speed, 'surface':pygame.transform.scale(BulletImage, (Bullet_size, Bullet_size)),}
        print(newBullet)
        a_list.append(newBullet)
        return a_list
    
    def MoveBullet (a_list2) :
        for a in a_list2:
            if not reverseCheat and not slowCheat:
                a['rect'].move_ip(0, a['speed'])
            elif reverseCheat:
                a['rect'].move_ip(0, -5)
            elif slowCheat:
                a['rect'].move_ip(0, 1)
        return a_list2
    
    def DeleteBullet(bullet_list2) :
        for a in bullet_list2[:] :
            if a['rect'].bottom < 0 :
                bullet_list2.remove(a)
        return bullet_list2
    
    def BulletHasHitAsteroids(bullets, asteroids, score) :
        for a in asteroids[:] :
            for b in bullets[:] : 
                if b['rect'].colliderect(a['rect']):
                    asteroids.remove(a)
                    bullets.remove(b)
                    score += 50
        return bullets, asteroids, score
    

    def BulletHasHitDrones(bullets, spacedrones, score) : 
        for a in spacedrones[:] :
            for b in bullets[:] : 
                if b['rect'].colliderect(a['rect']):
                    spacedrones.remove(a)
                    bullets.remove(b)
                    score += 100
        return bullets, spacedrones, score 

    def BulletHasHitFighter(bullets, fighters, score):
        for a in fighters[:] :
            for b in bullets[:] : 
                if b['rect'].colliderect(a['rect']):
                    fighters.remove(a)
                    bullets.remove(b)
                    score += 200
        return bullets, fighters, score
    
