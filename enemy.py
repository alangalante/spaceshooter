import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, player):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0)) # Red enemy
        self.rect = self.image.get_rect()
        self.player = player
        self.speed = 2
        
        # Spawn logic: Pick a random side (Top, Bottom, Left, Right)
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            self.rect.x = random.randint(0, screen_width)
            self.rect.y = -self.rect.height
        elif side == 'bottom':
            self.rect.x = random.randint(0, screen_width)
            self.rect.y = screen_height
        elif side == 'left':
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, screen_height)
        elif side == 'right':
            self.rect.x = screen_width
            self.rect.y = random.randint(0, screen_height)
            
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)

    def update(self):
        # Move towards player
        # Vector from enemy to player
        direction = self.player.pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        
        self.pos += direction * self.speed
        self.rect.center = self.pos
