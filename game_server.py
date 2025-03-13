class GameServer:
    def __init__(self):
        self.players = {}  # Track players
        self.bullets = []  # Track bullets

    def shoot(self, shooter_id, x, y, angle):
        """Add a new bullet to the game."""
        bullet_speed = 5  # Match client BULLET_SPEED
        self.bullets.append({"shooter_id": shooter_id, "x": x, "y": y, "angle": angle, "speed": bullet_speed})

    def update(self):
        """Move bullets and check for collisions."""
        for bullet in self.bullets[:]:
            bullet["x"] += bullet["speed"] * math.cos(math.radians(bullet["angle"]))
            bullet["y"] += bullet["speed"] * math.sin(math.radians(bullet["angle"]))

            if self.check_collision(bullet):
                self.bullets.remove(bullet)

    def check_collision(self, bullet):
        """Check if a bullet hits a player."""
        for player_id, player in self.players.items():
            if player_id != bullet["shooter_id"]:  # Can't hit yourself
                if self.is_collision(player["x"], player["y"], bullet["x"], bullet["y"]):
                    print(f"Player {player_id} was hit by {bullet['shooter_id']}")
                    return True
        return False

    def is_collision(self, px, py, bx, by):
        """Check if bullet (bx, by) is close to player (px, py)."""
        return abs(px - bx) < 20 and abs(py - by) < 20  # Adjust hitbox size
