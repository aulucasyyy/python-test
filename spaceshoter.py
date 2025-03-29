import pygame
import random
import sys

# Initialize pygame  
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Initialize font for displaying score
pygame.font.init()
font = pygame.font.SysFont(None, 36)

# Initialize score
score = 0

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self, *args):  # Update method to handle mouse movement
        mouse_x, _ = pygame.mouse.get_pos()
        self.rect.centerx = mouse_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 6)

    def update(self, *args):  # Accept additional arguments
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(2, 6)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self, *args):  # Accept additional arguments
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

def show_welcome_screen():
    # Set up welcome screen
    welcome_font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)
    welcome_text = welcome_font.render("Welcome to Lucas's Game of Space Shooter", True, WHITE)
    start_button_text = button_font.render("START", True, BLACK)
    
    # Button dimensions
    button_width, button_height = 200, 50
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2 + 100
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    while True:
        screen.fill(BLACK)
        screen.blit(welcome_text, ((WIDTH - welcome_text.get_width()) // 2, HEIGHT // 2 - 100))
        pygame.draw.rect(screen, WHITE, button_rect)
        screen.blit(start_button_text, (button_x + (button_width - start_button_text.get_width()) // 2, 
                                        button_y + (button_height - start_button_text.get_height()) // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):  # Left click on START button
                    return

def show_game_over_screen(final_score):
    # Set up game over screen
    game_over_font = pygame.font.SysFont(None, 72)
    button_font = pygame.font.SysFont(None, 36)
    game_over_text = game_over_font.render("GAME OVER", True, WHITE)
    score_text = button_font.render(f"Your Score: {final_score}", True, WHITE)
    play_again_text = button_font.render("PLAY AGAIN", True, BLACK)
    
    # Button dimensions
    button_width, button_height = 200, 50
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2 + 100
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    while True:
        screen.fill(BLACK)
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 150))
        screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2 - 50))
        pygame.draw.rect(screen, WHITE, button_rect)
        screen.blit(play_again_text, (button_x + (button_width - play_again_text.get_width()) // 2, 
                                      button_y + (button_height - play_again_text.get_height()) // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):  # Left click on PLAY AGAIN button
                    return

# Initialize firing timer
firing = False
firing_timer = 0
firing_interval = 0.000001  # Interval in seconds

# Main execution
if __name__ == "__main__":
    while True:
        show_welcome_screen()

        # Reset score and game state
        score = 0
        all_sprites.empty()
        enemies.empty()
        bullets.empty()

        # Recreate player and enemies
        player = Player()
        all_sprites.add(player)
        for _ in range(8):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Game loop
        running = True
        while running:
            clock.tick(60)
            current_time = pygame.time.get_ticks() / 1000  # Get current time in seconds

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        firing = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        firing = False

            # Handle continuous firing
            if firing and current_time - firing_timer >= firing_interval:
                player.shoot()
                firing_timer = current_time

            # Update
            all_sprites.update()

            # Check for collisions
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 10  # Increment score by 10
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

            if pygame.sprite.spritecollideany(player, enemies):
                running = False

            # Draw
            screen.fill(BLACK)
            all_sprites.draw(screen)

            # Render score
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()

        # Show game over screen
        show_game_over_screen(score)
