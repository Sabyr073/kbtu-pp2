import pygame
import sys
import random
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# -----------------------------
# GAME SETTINGS
# -----------------------------
FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

# -----------------------------
# COLORS
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
RED = (255, 0, 0)

# -----------------------------
# LOAD ASSETS
# -----------------------------
background = pygame.image.load("AnimatedStreet.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_img = pygame.image.load("Player.png")
player_img = pygame.transform.scale(player_img, (50, 90))

enemy_img = pygame.image.load("Enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 90))

# sounds
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)   # -1 means loop forever

crash_sound = pygame.mixer.Sound("crash.wav")

# fonts
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)

# game variables
enemy_speed = 7
coins_collected = 0
passed_enemies = 0

# -----------------------------
# PLAYER CLASS
# -----------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# -----------------------------
# ENEMY CLASS
# -----------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -60)

    def move(self):
        global passed_enemies
        self.rect.move_ip(0, enemy_speed)

        if self.rect.top > SCREEN_HEIGHT:
            passed_enemies += 1
            self.reset_position()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# -----------------------------
# COIN CLASS
# -----------------------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 12
        self.spawn()

    def spawn(self):
        self.x = random.randint(35, SCREEN_WIDTH - 35)
        self.y = random.randint(-600, -50)
        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def move(self):
        self.y += enemy_speed
        self.rect.center = (self.x, self.y)

        if self.y > SCREEN_HEIGHT + 20:
            self.spawn()

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, BLACK, (self.x, self.y), self.radius, 2)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def show_info():
    """
    Draw counters in the top corners.
    """
    passed_text = font.render(f"Passed: {passed_enemies}", True, WHITE)
    coins_text = font.render(f"Coins: {coins_collected}", True, WHITE)

    DISPLAYSURF.blit(passed_text, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))

def game_over():
    """
    Stop music, play crash sound, show Game Over screen.
    """
    pygame.mixer.music.stop()
    crash_sound.play()

    DISPLAYSURF.fill(BLACK)
    game_over_text = big_font.render("GAME OVER", True, RED)
    coins_text = font.render(f"Coins: {coins_collected}", True, WHITE)

    DISPLAYSURF.blit(
        game_over_text,
        game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    )

    DISPLAYSURF.blit(
        coins_text,
        coins_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
    )

    pygame.display.update()
    pygame.time.delay(2500)
    pygame.quit()
    sys.exit()

# -----------------------------
# CREATE OBJECTS
# -----------------------------
P1 = Player()
E1 = Enemy()
coin = Coin()

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # update objects
    P1.update()
    E1.move()
    coin.move()

    # collision with coin
    if P1.rect.colliderect(coin.rect):
        coins_collected += 1
        coin.spawn()

    # collision with enemy
    if P1.rect.colliderect(E1.rect):
        game_over()

    # draw everything
    DISPLAYSURF.blit(background, (0, 0))
    coin.draw(DISPLAYSURF)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    show_info()

    pygame.display.update()
    FramePerSec.tick(FPS)