import pygame
import time
from settings import TANK_MOVE_DELAY

class Tank:
    def __init__(self, x=50, y=50, speed=10, image="./tank image/Screenshot_5.png", tank_id=0, walls=[]):
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
        self.tank_id = tank_id
        self.offset = 0

    def move(self, keys, walls=None):
        if walls is None:
            walls = []

        self.prev_x = self.x
        self.prev_y = self.y

        current_time = time.time()
        if current_time - self.last_move_time < TANK_MOVE_DELAY:
            return

        # Calculate the potential new position based on the keys pressed
        new_x = self.x
        new_y = self.y

        """
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            new_y -= self.speed / 1.414
            new_x += self.speed / 1.414
            self.direction = 1
            self.image = pygame.transform.rotate(self.original_image, 45)
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            new_y -= self.speed / 1.414
            new_x -= self.speed / 1.414
            self.direction = 7
            self.image = pygame.transform.rotate(self.original_image, 135)
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            new_y += self.speed / 1.414
            new_x += self.speed / 1.414
            self.direction = 3
            self.image = pygame.transform.rotate(self.original_image, -45)
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            new_y += self.speed / 1.414
            new_x -= self.speed / 1.414
            self.direction = 5
            self.image = pygame.transform.rotate(self.original_image, -135)
        """
        if keys[pygame.K_UP]:
            new_y -= self.speed
            self.direction = 0
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif keys[pygame.K_DOWN]:
            new_y += self.speed
            self.direction = 4
            self.image = pygame.transform.rotate(self.original_image, -90)
        elif keys[pygame.K_LEFT]:
            new_x -= self.speed
            self.direction = 6
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif keys[pygame.K_RIGHT]:
            new_x += self.speed
            self.direction = 2
            self.image = pygame.transform.rotate(self.original_image, 0)


        if new_x < 50:
            new_x = 50  # Prevent moving left off the screen
        elif new_x + self.rect.width > 650+50:
            new_x = 650+50 - self.rect.width  # Prevent moving right off the screen

        if new_y < 50:
            new_y = 50  # Prevent moving up off the screen
        elif new_y + self.rect.height > 650+50:
            new_y = 650+50 - self.rect.height  # Prevent moving down off the screen
        # Check if the tank will collide with any wall at the new position
        if not self.check_wall_collision(new_x, new_y, walls):
            self.x = new_x
            self.y = new_y

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

    def check_wall_collision(self, new_x, new_y, walls):
        # Create a temporary rect for the new position, but make it smaller
        temp_rect = self.image.get_rect(topleft=(new_x, new_y))

        # Reduce the size of the temporary rectangle (e.g., by 10 pixels)
        smaller_rect = temp_rect.inflate(-10, -10)  # Reduce by 10px in both width and height

        # Check for collisions with walls
        for wall in walls:
            if smaller_rect.colliderect(wall.rect):
                # Adjust the tank's position to stop at the offset distance
                if new_x > self.x:  # Moving right
                    self.x = wall.rect.left - self.rect.width - self.offset
                elif new_x < self.x:  # Moving left
                    self.x = wall.rect.right + self.offset

                if new_y > self.y:  # Moving down
                    self.y = wall.rect.top - self.rect.height - self.offset
                elif new_y < self.y:  # Moving up
                    self.y = wall.rect.bottom + self.offset

                return True  # A collision was detected
        return False  # No collision detected


