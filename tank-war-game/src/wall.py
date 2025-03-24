import pygame

class Wall:
    def __init__(self, x, y, width, height, wall_id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load("./tank image/brick_wall.jpg")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health = 10
        self.alive = True
        self.wall_id = wall_id
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

