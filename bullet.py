import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))  # Yellow bullet
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.angle = angle
        
        # Calculate velocity based on angle
        # Convert angle to radians. Note: pygame angles are negative of standard math angles usually
        # But here we pass the angle from player rotation which was calculated as:
        # (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        # To get back direction vector we need careful conversion or just re-calculate from mouse pos
        # Easier to just pass the direction vector or rotation angle.
        # Let's assume angle is passed in degrees as per player's rotation.
        
        # Adjust angle to match trigonometric standard (0 is right, growing counter-clockwise)
        # Player angle: 0 is Up (due to -90 adjustment in player.py), and grows clockwise?
        # Let's look at player.py again.
        # angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        # If cursor is directly above: rel_x=0, rel_y<0. atan2(-y, 0) = -pi/2. -(-pi/2) = pi/2. 90 deg. 90-90=0. Correct.
        # So 0 IS UP.
        
        rad_angle = math.radians(self.angle + 90) # Add 90 to converting back to standard trig (where 0 is Right)
        # Actually, let's just use vector math if we can, but since we have angle...
        
        # Standard trig: 0 is Right. 90 is Up (in standard cartesian), but in Pygame Y is down.
        # So 90 being Up means -Y direction.
        # cos(90) = 0, sin(90) = 1. We want (0, -1). 
        # So we probably want: x = cos(a), y = -sin(a)?
        
        # Let's simplify. I will just pass the angle to rotate the bullet image too?
        # Nah, bullet is a square for now.
        
        self.vx = math.cos(rad_angle) * self.speed
        self.vy = -math.sin(rad_angle) * self.speed # Negative because Y grows down
        
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Kill if off screen
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()
