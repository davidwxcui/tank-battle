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
        self.direction = 2 #2 is right
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_move_time = time.time()
        self.health = 1
        self.alive = True

        #attributes needed for powerup processing
        self.active_powerup = None


    def move(self, keys):
        self.prev_x = self.x
        self.prev_y = self.y

        current_time = time.time()
        if current_time - self.last_move_time < TANK_MOVE_DELAY:
            return
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.y -= self.speed/1.414
            self.x += self.speed/1.414
            self.direction = 1
            self.image = pygame.transform.rotate(self.original_image, 45)
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.y -= self.speed/1.414
            self.x -= self.speed/1.414
            self.direction = 7
            self.image = pygame.transform.rotate(self.original_image, 135)
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.y += self.speed/1.414
            self.x += self.speed/1.414
            self.direction = 3
            self.image = pygame.transform.rotate(self.original_image, -45)
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.y += self.speed/1.414
            self.x -= self.speed/1.414
            self.direction = 5
            self.image = pygame.transform.rotate(self.original_image, -135)
        elif keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = 0
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = 4
            self.image = pygame.transform.rotate(self.original_image, -90)
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = 6
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = 2
            self.image = pygame.transform.rotate(self.original_image, 0)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_move_time = current_time


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_location(self):
        return self.x, self.y

    def set_direction(self, direction):
        self.direction = direction
        if direction == 0:
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif direction == 1:
            self.image = pygame.transform.rotate(self.original_image, 45)
        elif direction == 2:
            self.image = pygame.transform.rotate(self.original_image, 0)
        elif direction == 3:
            self.image = pygame.transform.rotate(self.original_image, -45)
        elif direction == 4:
            self.image = pygame.transform.rotate(self.original_image, -90)
        elif direction == 5:
            self.image = pygame.transform.rotate(self.original_image, -135)
        elif direction == 6:
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif direction == 7:
            self.image = pygame.transform.rotate(self.original_image, 135)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def detect_collision_tank(self, other_tank):
        return self.rect.colliderect(other_tank.rect)

    def get_health(self):
        return self.health
    
    def death(self):
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def is_alive(self):
        return self.alive

    def take_damage(self):
        self.health -= 1

    


