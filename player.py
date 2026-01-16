import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__()
        # Create a simple triangle surface for the player
        self.original_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Draw a triangle
        pygame.draw.polygon(self.original_image, (0, 255, 0), [(15, 0), (0, 30), (30, 30)])
        
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.speed = 5
        self.pos = pygame.math.Vector2(x, y)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.angle = 0

    def update(self, move_vector=None, shoot_trigger=False):
        self.input(move_vector)
        self.rotate()
        self.constrain()
        return shoot_trigger

    def input(self, external_vector=None):
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0

        # Keyboard Input
        if keys[pygame.K_UP]:
            move_y = -1
        if keys[pygame.K_DOWN]:
            move_y = 1
        if keys[pygame.K_LEFT]:
            move_x = -1
        if keys[pygame.K_RIGHT]:
            move_x = 1

        # Combine with external vector (Virtual Joystick)
        if external_vector:
            move_x += external_vector.x
            move_y += external_vector.y
        
        # Apply movement
        if move_x != 0 or move_y != 0:
            move_vector_final = pygame.math.Vector2(move_x, move_y)
            # Clamp length to 1 to avoid double speed if using both inputs (though unlikely)
            if move_vector_final.length() > 1:
                move_vector_final = move_vector_final.normalize()
            elif move_vector_final.length() > 0 and not external_vector:
                 # Normalize keyboard input which is always length 1 or 1.414
                 move_vector_final = move_vector_final.normalize()
            
            self.pos += move_vector_final * self.speed
            self.rect.center = self.pos

    def constrain(self):
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.pos.x = self.rect.centerx
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
            self.pos.y = self.rect.centery

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        
        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        # We need to return a bullet creation instruction or return the bullet object
        # But Player doesn't import Bullet to avoid circular imports if possible,
        # or we update main to create bullet.
        # Let's instantiate Bullet here.
        from bullet import Bullet
        return Bullet(self.rect.centerx, self.rect.centery, self.angle)

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        
        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)
