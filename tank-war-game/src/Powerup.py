import pygame
import time
from settings import FPS
class Powerup:
    def __init__(self, x, y, power_type, image="./powerup image/explosion2.png"):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.is_visible = True #available to collect
        self.is_active = False #Active after tank collides
        
        original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x,y))
        

    def draw(self, screen):
        if self.is_visible:
            screen.blit(self.image, (self.x, self.y))

    def activate(self, tank):
        if self.is_visible:
            self.is_visible = False
            self.is_active = True

            if self.power_type == "speed":
                tank.speed *= 2

            if self.power_type == "health":
                tank.health = 200000000000
            #will add more types later

            tank.active_powerup = self.power_type

    def deactivate(self, tank):
        #once duration expires go back to normal
        if self.is_active:
            if self.power_type == "speed":
                tank.speed /= 2

            if self.power_type == "health":
                tank.health = 1

            #will add the others lateer
            self.is_active = False
            tank.active_powerup = None
            tank.powerup_timer = 0

