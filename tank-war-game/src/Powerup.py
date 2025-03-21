import pygame
import time
from settings import FPS
class Powerup:
    def __init__(self, x, y, power_type, duration, image="./powerup image/explosion2.png"):
        self.x = x
        self.y = x
        self.power_type = power_type
        self.duration = duration
        self.is_visible = True #available to collect
        self.is_active = False #Active after tank collides
        self.timer = 0
        
        original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x,y))
        

    def draw(self, screen):
        if self.is_visible:
            screen.blit(self.image, (self.x, self.y))

    def check_collision(self, tank):
        return self.is_visible and self.rect.colliderect(tank.rect)

    def activate(self, tank):
        if self.is_visible:
            self.is_visible = False
            self.is_active = True
            self.timer = self.duration

            if self.power_type == "speed":
                tank.speed *= 1.5
            #will add more types later

            tank.active_powerup = self.power_type
            tank.powerup_timer = self.duration

    def deactivate(self, tank):
        #once duration expires go back to normal
        if self.is_active:
            if self.power_type == "speed":
                tank.speed /= 1.5


            #will add the others lateer
            self.is_active = False
            tank.active_powerup = None

    def update(self, tank):
        if self.is_active:
            self.timer -= 1 / FPS
            if self.timer <= 0:
                self.deactivate(tank)
    
