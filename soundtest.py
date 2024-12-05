import pygame # Initialize Pygame and the mixer 
pygame.init() 
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512) # Load the sound file 
try: 
    sound = pygame.mixer.Sound('Boom2.wav') 
except pygame.error as e: 
    print(f"Error loading sound: {e}") 
    pygame.quit() 
    raise # Play the sound 

sound.play() # Wait long enough to hear the sound 
pygame.quit