import os
import sys
import pygame
from tank import Tank
from cannonball import Cannonball
from settings import *
from wall import Wall
import struct
import socket
import random
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import time

# Define consta
#Using this for debugging purposes
WIDTH, HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT # Screen size
CELL_SIZE = 50  # Size of each grid cell
GRID_COLOR = (200, 200, 200)  # Light gray grid lines
TEXT_COLOR = (255, 0, 0)  # Red text for coordinates




class Game:
    def __init__(self,x=50, y=50, id=0,client_name=None):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Tank War Game")
        self.clock = pygame.time.Clock()
        self.tank = Tank(x,y)
        self.cannonballs = []
        self.running = True
        self.last_shot_time = 0
        self.opponents = []  # List to store opponent tanks
        self.opponents_id = []
        self.id = id # id of the player
        self.shots = {} # dictionary to store the shots
        self.Walls = []
        self.received_all_walls = False
        self.kills = 0
        self.health= 1
        self.game_state= 0 # 0 is start screen, 1 is game loop, 2 is end screen
        self.waiting_for_start = True

        pygame.display.set_caption(f"Tank War - {id} - {client_name}")  # Change the title to "Tank War"
        print(f"Game initialized with id: {id}")
    #Draws a grid on the screen with coordinates for debugging purposes
    def draw_grid(self):
            font = pygame.font.Font(None, 24)  # Define font inside the function
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))
                for y in range(0, HEIGHT, CELL_SIZE):
                    pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))
                    coord_text = font.render(f"({x},{y})", True, TEXT_COLOR)
                    self.screen.blit(coord_text, (x + 2, y + 2))  # Offset text for visibility

    def draw_start_screen(self):
        self.screen.fill(UI_BOARD_COLOR)
        font= pygame.font.Font(None, 36)
        start_text = font.render("Press Enter to Start", True, TEXT_COLOR)
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
        pygame.display.flip()

    def draw_end_screen(self):
        self.screen.fill(UI_BOARD_COLOR)
        font= pygame.font.Font(None, 36)
        end_text = font.render("Game Over", True, TEXT_COLOR)
        self.screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - end_text.get_height() // 2))
        kills_text = font.render(f"Kills: {self.kills}", True, TEXT_COLOR)
        self.screen.blit(kills_text, (SCREEN_WIDTH // 2 - kills_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()


    def run(self, s=None):
        self.game_state = 0  # Ensure game state starts with the start screen
        self.draw_start_screen()  # Show the start screen first
        while self.waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running =  False
                    self.waiting_for_start = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Start the game when Enter is pressed
                        self.waiting_for_start = False
                        self.game_state = 1  # Move to game loop state
                        self.game_loop(s)

    def game_loop(self, s=None):
        while self.running:
            if self.game_state == 0:
                self.draw_start_screen()  # Redraw start screen if game state is 0
            elif self.game_state == 1:
                self.handle_events(s)
                self.update(s)
                self.draw()
            elif self.game_state == 2:
                self.draw_end_screen()  # Show end screen if game state is 2
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
        self.tank.move(keys, self.Walls)
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
            #cannonball = Cannonball(self.tank.rect.centerx, self.tank.rect.centery, self.tank.direction, self.id, CANNONBALL_SPEED)
            #self.cannonballs.append(cannonball)
            self.last_shot_time = current_time
            if s:  # Only send if socket exists
                msg_type = 2
                x = int(self.tank.rect.centerx)
                y = int(self.tank.rect.centery)
                direction = int(self.tank.direction)
                token = struct.pack("!BIhhH", msg_type, self.id,  x, y, direction)
                s.sendall(token)
                print(f"Shooting message sent id{self.id} x{x} y{y} direction{direction}")

    def update(self, s= None):
        for cannonball in self.cannonballs:
            cannonball.update()
            if cannonball.is_out_of_bounds():
                self.cannonballs.remove(cannonball)
        self.check_tank_collision()
        #self.check_cannonball_collision(s)


    def draw(self):
        #self.screen.fill(BACKGROUND_COLOR)
        self.screen.fill(UI_BOARD_COLOR)
        self.screen.fill(GAME_BOARD_COLOR, (50,50,650,650))
        self.tank.draw(self.screen)
        for opponent in self.opponents:
            opponent.draw(self.screen)
        for cannonball in self.cannonballs:
            cannonball.draw(self.screen)
        #if self.received_all_walls:
        for wall in self.Walls:
            wall.draw(self.screen)
        #use this to draw a grid on the screen for debugging purposes
        #self.draw_grid() 
        font= pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {self.health}", True, TEXT_COLOR)
        self.screen.blit(health_text, (710, 550))
        kills_text = font.render(f"Kills: {self.kills}", True, TEXT_COLOR)
        self.screen.blit(kills_text, (710, 600))

        pygame.display.flip()

    def add_opponent(self, x, y, id):
        opponent = Tank(x, y,id)
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

    def update_all_shooting(self, id, shot_id, x, y, direction):
        if id == self.id:
            cannonball = Cannonball(self.tank.rect.centerx, self.tank.rect.centery, self.tank.direction, self.id, shot_id,CANNONBALL_SPEED)
            self.cannonballs.append(cannonball)
        else:
            self.update_opponent_shooting(id, shot_id, x, y, direction)
    
    
    def update_opponent_shooting(self, id, shot_id, x, y, direction):
        for opponent_id in self.opponents_id:
            if id == opponent_id:
                index = self.opponents_id.index(opponent_id)
                # Update the opponent's position
                self.opponents[index].set_direction(direction)

                # Get the tank's rectangle center position
                offsetx = self.opponents[index].rect.centerx
                offsety = self.opponents[index].rect.centery
                print(f"Offset: {offsetx}, {offsety}")

                # Create and append the cannonball with the adjusted position
                cannonball = Cannonball(x, y, direction, id, shot_id,CANNONBALL_SPEED)
                self.cannonballs.append(cannonball)
                break

                
    def check_tank_collision(self):
        for opponent in self.opponents:
            if self.tank.detect_collision_tank(opponent):
                print("Collision detected")
                self.handle_tank_collision()
                break
    
    def handle_tank_collision(self):
        self.tank.x = self.tank.prev_x
        self.tank.y = self.tank.prev_y

    def check_cannonball_collision(self, s= None):
        # Need to iterate over a copy of the list since we're modifying it
        for cannonball in self.cannonballs[:]:
            # Check if cannonball hits any opponent
            for opponent in self.opponents:
                index = self.opponents.index(opponent)
                opponent_id = self.opponents_id[index]
                
                # Only check collision if the shooter is not hitting themselves
                
                if cannonball.shooter_id != opponent_id:
                    print(f"Cannonball shooter_id{cannonball.shooter_id} is not the same as the cannonball shooter_id{opponent_id}")
                    if cannonball.check_collision_cannonball_tank(opponent, opponent_id, cannonball.shooter_id):
                        print("HIT!")
                        if cannonball in self.cannonballs:  # Check if cannonball still exists
                            self.cannonballs.remove(cannonball)
                        self.send_cannonball_hit(opponent, opponent_id, s)
                        break

    def send_cannonball_hit(self, opponent, opponent_id, s):
        msg_type = 3
        x = int(opponent.x)
        y = int(opponent.y)
        player_id = int(self.id)
        send_opponent_id = int(opponent_id)
        token = struct.pack("!BIhhH", msg_type, player_id, send_opponent_id, x, y)
        if s:  # Only send if socket connection exists
            s.sendall(token)
            print(f"Cannonball hit message sent player_id{player_id} opponent_id{send_opponent_id} x{x} y{y}")
 

    def handle_cannonball_hit(self, player_hitter_id, player_hit_id, bullet_id):
        if player_hit_id == self.id:
            self.health -= 1
        for cannonball in self.cannonballs:
            if cannonball.shot_id == bullet_id:
                self.cannonballs.remove(cannonball)
                break

    def handle_player_eliminated(self, player_hitter_id, player_id):
        if player_id == self.id:
            self.game_state = 2
            print(f"Player {player_id} has been eliminated!")
            self.running = False
        else:
            if player_hitter_id == self.id: 
                self.kills += 1
            # Remove the opponent from the list if they are eliminated
            if player_id in self.opponents_id:
                print(f"Player {player_id} is in the opponents id list")
                index = self.opponents_id.index(player_id)
                # Check that the opponent's tank ID matches
                for opponent in self.opponents:
                    print(opponent)
                #if self.opponents[index] == player_id:
                print(f"Player {player_id} is in the opponents list")
                del self.opponents[index]  # Delete opponent tank from the list
                del self.opponents_id[index]  # Delete opponent's ID from the list
                print(f"Player {player_id} has been eliminated!")

    def handle_wall_data(self, x, y, width, height, wall_id):
        for wall in self.Walls:
            if wall.wall_id == wall_id:
                return  # Skip if wall already exists
        self.Walls.append(Wall(x, y, width, height, wall_id))

    def handle_wall_hit(self, bullet_id):
        for cannonball in self.cannonballs:
            if cannonball.shot_id == bullet_id:
                self.cannonballs.remove(cannonball)
                break

    def handle_wall_destroy(self,  wall_id,bullet_id):
        self.handle_wall_hit(bullet_id)
        for wall in self.Walls:
            if wall.wall_id == wall_id:
                self.Walls.remove(wall)
                print(f"Client side Wall {wall_id} destroyed!")
                break
        


if __name__ == "__main__":
    game = Game()
    # game.add_opponent(200, 200)
    game.run()