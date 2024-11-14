import pygame, random, sys
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
AsteroidImage = pygame.image.load('Asteroids.png')
reverseCheat = slowCheat = False

class Asteroids (): 
    asteroids_min_size = 10 
    asteroids_max_size = 40
    asteroids_min_speed = 1 
    asteroids_max_speed = 8 

    def CreateNewAsteroids(a_list) : 
        asteroids_size = random.randint(Asteroids.asteroids_min_size, Asteroids.asteroids_max_size)
        newAsteroid = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - asteroids_size), 0 - asteroids_size, asteroids_size, asteroids_size), 'speed': random.randint(Asteroids.asteroids_min_speed, Asteroids.asteroids_max_speed), 'surface':pygame.transform.scale(AsteroidImage, (asteroids_size, asteroids_size)),}
        print(newAsteroid)
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