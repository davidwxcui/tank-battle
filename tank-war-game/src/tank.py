import pygame
import time
from settings import TANK_MOVE_DELAY

class Tank:
    def __init__(self, x=100, y=100, speed=10, image="./tank image/Screenshot_5.png"):
        self.x = x
        self.y = y
        self.speed = speed
        self.original_image = pygame.image.load(image)
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.direction = 'right'
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_move_time = time.time()


    def move(self, keys):
        current_time = time.time()
        if current_time - self.last_move_time < TANK_MOVE_DELAY:
            return
        
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.y -= self.speed/1.414
            self.x += self.speed/1.414
            self.direction = 'up-right'
            self.image = pygame.transform.rotate(self.original_image, 45)
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.y -= self.speed/1.414
            self.x -= self.speed/1.414
            self.direction = 'up-left'
            self.image = pygame.transform.rotate(self.original_image, 135)
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.y += self.speed/1.414
            self.x += self.speed/1.414
            self.direction = 'down-right'
            self.image = pygame.transform.rotate(self.original_image, -45)
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.y += self.speed/1.414
            self.x -= self.speed/1.414
            self.direction = 'down-left'
            self.image = pygame.transform.rotate(self.original_image, -135)
        elif keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = 'up'
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = 'down'
            self.image = pygame.transform.rotate(self.original_image, -90)
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = 'left'
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = 'right'
            self.image = pygame.transform.rotate(self.original_image, 0)


        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_move_time = current_time

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


