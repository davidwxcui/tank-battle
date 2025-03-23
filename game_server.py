import sys
import os
import threading
import time
import math
import pygame
import struct
from pygame.locals import *
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CANNONBALL_SPEED

sys.path.insert(0, os.path.abspath('./tank-war-game/src'))

class GameServer:
    def __init__(self, broadcast_func_to_all, broadcast_func_to_client):
        self.broadcast_func_to_all = broadcast_func_to_all
        self.broadcast_func_except_sender = broadcast_func_to_client

        self.players = {}  # {player_id: {"rect": pygame.Rect, "dir": int, "health": int}}
        self.bullets = {}  # {bullet_id: {"rect": pygame.Rect, "owner": player_id}}
        self.lock = threading.Lock()  # Ensures thread safety
        self.game_thread = threading.Thread(target=self.update_game_state, daemon=True)
        self.game_thread.start()  # Start the game loop in a background thread
        self.bullet_shot = 0

    def add_player(self, player_id, x, y, width, height, direction):
        """Add a new player safely using pygame.Rect for player position."""
        with self.lock:
            player_rect = pygame.Rect(x, y, width, height)
            self.players[player_id] = {"rect": player_rect, "dir": direction, "health": 1}

    def move_player(self, player_id, new_x, new_y, direction):
        """Move a player safely, updating their position in the Rect."""
        with self.lock:
            if player_id in self.players:
                self.players[player_id]["rect"].x = new_x
                self.players[player_id]["rect"].y = new_y
                self.players[player_id]["dir"] = direction

    #add a bullet to the game state and send it to all clients including the shooter 
    def add_bullet(self, shooter_id, x, y,  direction):
        """Add a new bullet safely using pygame.Rect for the bullet."""
        with self.lock:
            bullet_rect = pygame.Rect(x, y, 5, 5)  # Set the size of the bullet
            bullet_id = self.bullet_shot
            self.bullet_shot += 1
            self.bullets[bullet_id] = {"rect": bullet_rect, "owner": shooter_id, "bullet_direction": direction}
            msg_type=2
            packed_data = struct.pack('!Hhhhhh', msg_type, shooter_id, bullet_id, x, y, direction)
            self.broadcast_func_to_all(packed_data)
            
    def update_game_state(self):
        """Main game loop to update positions and check for collisions."""
        while True:
            with self.lock:
                # Move all bullets
                for bullet_id, bullet in list(self.bullets.items()):
                    direction = bullet["bullet_direction"]

                    # Update bullet position based on direction
                    if direction == 0:  # Up
                        bullet["rect"].y -= CANNONBALL_SPEED
                    elif direction == 4:  # Down
                        bullet["rect"].y += CANNONBALL_SPEED
                    elif direction == 6:  # Left
                        bullet["rect"].x -= CANNONBALL_SPEED
                    elif direction == 2:  # Right
                        bullet["rect"].x += CANNONBALL_SPEED
                    elif direction == 1:  # Up-Right
                        bullet["rect"].y -= CANNONBALL_SPEED / 1.414
                        bullet["rect"].x += CANNONBALL_SPEED / 1.414
                    elif direction == 7:  # Up-Left
                        bullet["rect"].y -= CANNONBALL_SPEED / 1.414
                        bullet["rect"].x -= CANNONBALL_SPEED / 1.414
                    elif direction == 3:  # Down-Right
                        bullet["rect"].y += CANNONBALL_SPEED / 1.414
                        bullet["rect"].x += CANNONBALL_SPEED / 1.414
                    elif direction == 5:  # Down-Left
                        bullet["rect"].y += CANNONBALL_SPEED / 1.414
                        bullet["rect"].x -= CANNONBALL_SPEED / 1.414

                    # Check if the bullet hits any player
                    for player_id, player in list(self.players.items()):
                        if player_id != bullet["owner"]:
                            #print(f"Player Rect: {player['rect']}, Bullet Rect: {bullet['rect']}")
                            collide = pygame.Rect.colliderect(bullet["rect"], player["rect"])
                            #print(f"Collision detected: {collide}")
                            
                            if collide:
                                print(f"Player {player_id} was hit by Player {bullet['owner']}! with bullet id {bullet_id}")
                                msg_type=3
                                player_hitter_id= bullet['owner']
                                player_hit_id= player_id
                                self.broadcast_func_to_all(struct.pack('!Hhhh', msg_type, player_hitter_id, player_hit_id, bullet_id))
                                player["health"] -= 1
                                del self.bullets[bullet_id]
                                if player["health"] <= 0:
                                    print(f"Player {player_id} has been eliminated!")
                                    del self.players[player_id]
                                    msg_type=6
                                    self.broadcast_func_to_all(struct.pack('!Hh', msg_type, player_hit_id))
                                break  # Stop checking once bullet hits someone

                    # Remove bullets if they go off-screen
                    if bullet_id in self.bullets:  # Ensure the bullet wasn't removed in collision check
                        if bullet["rect"].x < 0 or bullet["rect"].x > SCREEN_WIDTH or bullet["rect"].y < 0 or bullet["rect"].y > SCREEN_HEIGHT:
                            del self.bullets[bullet_id]

            time.sleep(1 / FPS)  # Maintain the game FPS (30 updates per second)

    def get_game_state(self):
        """Return a snapshot of the current game state (thread-safe)."""
        with self.lock:
            return self.players.copy(), self.bullets.copy()
