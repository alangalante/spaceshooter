import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (30, 30, 30)

from player import Player
from enemy import Enemy
from ui import VirtualJoystick, TouchButton

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # Create Player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.all_sprites.add(self.player)

        # Enemy spawn event
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 500) # Spawn every 500ms

        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 72)
        
        # UI controls
        # Joystick bottom left
        self.joystick = VirtualJoystick(100, SCREEN_HEIGHT - 100, 60)
        # Fire button bottom right
        self.fire_button = TouchButton(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 40)
        self.fire_cooldown = 0 # To prevent stream of bullets from rapid update loop with button held

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.all_sprites.add(self.player)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if not self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: # Space check
                        bullet = self.player.shoot()
                        self.all_sprites.add(bullet)
                        self.bullets.add(bullet)
                elif event.type == self.ADDENEMY:
                    new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, self.player)
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()

    def update(self):
        if self.game_over:
            return

        # Update UI inputs
        events = pygame.event.get() # Actually we handle events in handle_events, but UI needs 'continuous' state
        # The joystick.update checks pygame.mouse.get_pressed(), so just calling it is fine.
        self.joystick.update(None)
        self.fire_button.update(None)

        # Logic for firing from button
        if self.fire_button.active and self.fire_cooldown == 0:
             bullet = self.player.shoot()
             self.all_sprites.add(bullet)
             self.bullets.add(bullet)
             self.fire_cooldown = 15 # Delay frames
        
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        # Pass joystick vector to player
        self.player.update(self.joystick.input_vector)
        self.bullets.update()
        self.enemies.update()
        
        # Bullet hits Enemy
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        if hits:
            self.score += len(hits) * 10
            
        # Enemy hits Player
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.player.kill()
            self.game_over = True
            # self.running = False # Don't exit, show game over

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)
        
        # Draw Score
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))
        
        # Draw UI
        if not self.game_over:
            self.joystick.draw(self.screen)
            self.fire_button.draw(self.screen)
        
        if self.game_over:
            game_over_surface = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
            game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_surface, game_over_rect)
            
            restart_surface = self.font.render("Press 'R' to Play Again", True, (255, 255, 255))
            restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(restart_surface, restart_rect)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
