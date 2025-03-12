import os
import sys
import pygame
from tank import Tank
from cannonball import Cannonball
from settings import *
import struct
import socket
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Game:
    def __init__(self,x=100, y=100, id=0,client_name=None):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tank War Game")
        self.clock = pygame.time.Clock()
        self.tank = Tank(x,y)
        self.cannonballs = []
        self.running = True
        self.last_shot_time = 0
        self.opponents = []  # List to store opponent tanks
        self.opponents_id = []
        self.id = id
        pygame.display.set_caption(f"Tank War - {id} - {client_name}")  # Change the title to "Tank War"

    def run(self,s=None):
        while self.running:
            self.handle_events(s)
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self,s=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shoot(s)

        keys = pygame.key.get_pressed()
        self.tank.move(keys)
        if s and (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            msg_type = 1  # movement message type
            x = int(self.tank.x)
            y = int(self.tank.y)
            direction = int(self.tank.direction)
            token = struct.pack("!BIhhH", msg_type, self.id, x, y, direction)
            s.sendall(token)
            print(f"Movement message sent id{self.id} x{x} y{y} direction{direction}")
    


    def shoot(self,s):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > CANNONBALL_DELAY * 1000:
            cannonball = Cannonball(self.tank.rect.centerx, self.tank.rect.centery, self.tank.direction, CANNONBALL_SPEED)
            self.cannonballs.append(cannonball)
            self.last_shot_time = current_time
            msg_type = 2
            x = int(self.tank.x)
            y = int(self.tank.y)
            direction = int(self.tank.direction)
            token = struct.pack("!BIhhH", msg_type, self.id, x, y, direction)
            s.sendall(token)
            print(f"Shooting message sent id{self.id} x{x} y{y} direction{direction}")

    def update(self):
        for cannonball in self.cannonballs:
            cannonball.update()
            if cannonball.is_out_of_bounds():
                self.cannonballs.remove(cannonball)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.tank.draw(self.screen)
        for opponent in self.opponents:
            opponent.draw(self.screen)
        for cannonball in self.cannonballs:
            cannonball.draw(self.screen)
        pygame.display.flip()

    def add_opponent(self, x, y, id):
        opponent = Tank(x, y)
        self.opponents.append(opponent)
        self.opponents_id.append(id)

    def existing_opponent(self, id):
        for opponent_id in self.opponents_id:
            if id == opponent_id:
                return True
        return False

    def update_opponent(self, id, x, y, direction):
        for opponent_id in self.opponents_id:
            if id == opponent_id:
                index = self.opponents_id.index(opponent_id)
                self.opponents[index].x = x
                self.opponents[index].y = y
                self.opponents[index].set_direction(direction)  # Update the direction

    def update_opponent_shooting(self, id, x, y, direction):
        for opponent_id in self.opponents_id:
            if id == opponent_id:
                index = self.opponents_id.index(opponent_id)
                # Update the opponent's position
                self.opponents[index].x = x
                self.opponents[index].y = y
                self.opponents[index].set_direction(direction)
                
                # Use the opponent's rect to get the center position
                offsetx = self.opponents[index].rect.centerx
                offsety = self.opponents[index].rect.centery
                
                # Create and append a cannonball
                cannonball = Cannonball(offsetx, offsety, direction, CANNONBALL_SPEED)
                self.cannonballs.append(cannonball)
                
if __name__ == "__main__":
    game = Game()
    # game.add_opponent(200, 200)
    game.run()
    