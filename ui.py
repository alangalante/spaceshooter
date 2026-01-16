import pygame
import math

class VirtualJoystick:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.knob_radius = radius // 2
        self.knob_x = x
        self.knob_y = y
        self.active = False
        self.input_vector = pygame.math.Vector2(0, 0)
        self.pointer_id = None # To track multi-touch ID if needed (simplified for mouse/single touch)

    def update(self, events):
        # We need to handle touch events specifically or mouse as fallback
        # Pygame handles mouse as touch usually if not configured otherwise on mobile
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0] # Left click acts as touch

        # Logic for "is touched"
        # Since standard Pygame Desktop doesn't support multitouch without specific setup,
        # we will assume single pointer interactions for the desktop test, 
        # but on mobile this needs event loop handling for FINGERDOWN/FINGERMOVE.
        # For this prototype we will use mouse logic which maps well to single finger.
        
        dist = math.hypot(mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        
        if mouse_pressed:
            if self.active:
                # Already grabbing knob
                dx = mouse_pos[0] - self.x
                dy = mouse_pos[1] - self.y
                angle = math.atan2(dy, dx)
                current_dist = math.hypot(dx, dy)
                
                # Clamp knob to radius
                if current_dist > self.radius:
                    self.knob_x = self.x + math.cos(angle) * self.radius
                    self.knob_y = self.y + math.sin(angle) * self.radius
                else:
                    self.knob_x = mouse_pos[0]
                    self.knob_y = mouse_pos[1]
                
                # Calculate vector (-1 to 1)
                final_dx = self.knob_x - self.x
                final_dy = self.knob_y - self.y
                self.input_vector.x = final_dx / self.radius
                self.input_vector.y = final_dy / self.radius

            elif dist <= self.radius:
                 # Start grabbing
                 self.active = True
        else:
            # Release
            self.active = False
            self.knob_x = self.x
            self.knob_y = self.y
            self.input_vector.x = 0
            self.input_vector.y = 0

    def draw(self, screen):
        # Base
        pygame.draw.circle(screen, (100, 100, 100, 128), (self.x, self.y), self.radius)
        # Knob
        pygame.draw.circle(screen, (200, 200, 200, 200), (int(self.knob_x), int(self.knob_y)), self.knob_radius)


class TouchButton:
    def __init__(self, x, y, radius, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.active = False
        
    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        dist = math.hypot(mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        
        if mouse_pressed and dist <= self.radius:
            self.active = True
        else:
            self.active = False

    def draw(self, screen):
        color = self.color if not self.active else (255, 100, 100)
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius, 2)
        pygame.draw.circle(screen, (*color, 100), (self.x, self.y), self.radius - 5)
