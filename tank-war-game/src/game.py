import os
import sys
import pygame
from tank import Tank
from cannonball import Cannonball
from settings import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tank War Game")
        self.clock = pygame.time.Clock()
        self.tank = Tank()
        self.cannonballs = []
        self.running = True
        self.last_shot_time = 0

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shoot()

        keys = pygame.key.get_pressed()
        self.tank.move(keys)

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > CANNONBALL_DELAY * 1000:
            cannonball = Cannonball(self.tank.rect.centerx, self.tank.rect.centery, self.tank.direction, CANNONBALL_SPEED)
            self.cannonballs.append(cannonball)
            self.last_shot_time = current_time

    def update(self):
        for cannonball in self.cannonballs:
            cannonball.update()
            if cannonball.is_out_of_bounds():
                self.cannonballs.remove(cannonball)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.tank.draw(self.screen)
        for cannonball in self.cannonballs:
            cannonball.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()