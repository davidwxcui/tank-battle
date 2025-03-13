import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CANNONBALL_SPEED

class Cannonball:
    def __init__(self, x, y, direction, shooter_id, speed=CANNONBALL_SPEED):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.active = True
        self.shooter_id = shooter_id


    def update(self):
        if self.active:
            if self.direction == 0:
                self.y -= self.speed
            elif self.direction == 4:
                self.y += self.speed
            elif self.direction == 6:
                self.x -= self.speed
            elif self.direction == 2:
                self.x += self.speed
            elif self.direction == 1:
                self.y -= self.speed / 1.414
                self.x += self.speed / 1.414
            elif self.direction == 7:
                self.y -= self.speed / 1.414
                self.x -= self.speed / 1.414
            elif self.direction == 3:
                self.y += self.speed / 1.414
                self.x += self.speed / 1.414
            elif self.direction == 5:
                self.y += self.speed / 1.414
                self.x -= self.speed / 1.414

            #print(f"Cannonball Position: ({self.x}, {self.y})")

            # Check if the cannonball is out of bounds
            if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
                self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5)

    def check_collision_cannonball_tank(self, tank, opponent_id, shooter_id):
        # Don't check collision if the shooter is hitting their own cannonball
        if self.active == True:
            if shooter_id == self.shooter_id:
                return False
            # Create rectangles for collision detection
            cannonball_rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)  # Center the 10x10 rect on cannonball position
            # Check if the rectangles overlap
            if cannonball_rect.colliderect(tank.rect):
                self.active = False
                tank.take_damage()  # Reduce tank health when hit
                return True
                
            return False

    
    def is_out_of_bounds(self):
        return self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT
