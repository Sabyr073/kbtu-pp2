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

coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img,(30,30))

pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

crash_sound = pygame.mixer.Sound("crash.wav")

font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)

enemy_speed = 5
passed_enemies = 0
coin_speed = 5
collected_coins = 0
level = 1

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
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(30,SCREEN_WIDTH - 30), -50)
        self.value = random.randint(1,3)

    def move(self):
        global collected_coins
        self.rect.move_ip(0, coin_speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        value_text = font.render(str(self.value),True, WHITE)
        surface.blit(value_text,(self.rect.x + 9, self.rect.y + 3))





# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def show_info():

    passed_text = font.render(f"Passed: {passed_enemies}", True, WHITE)
    DISPLAYSURF.blit(passed_text, (10, 10))

def show_coins():
    
    collected_text = font.render(f"Coins: {collected_coins}", True, WHITE)
    DISPLAYSURF.blit(collected_text, (SCREEN_WIDTH - 105 ,10))

def show_level():
    level_text = font.render(f"Level: {level}",True,WHITE)
    DISPLAYSURF.blit(level_text,(SCREEN_WIDTH - 230 ,10))


def game_over():

    pygame.mixer.music.stop()
    crash_sound.play()

    DISPLAYSURF.fill(BLACK)
    game_over_text = big_font.render("GAME OVER", True, RED)
    collected_text = font.render(f"Collected coins: {collected_coins}", True, WHITE)
    passed_text = font.render(f"Passed cars: {passed_enemies}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    DISPLAYSURF.blit(
        game_over_text,
        game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    )

    DISPLAYSURF.blit(
        level_text,
        level_text.get_rect(center = (SCREEN_WIDTH // 2, 350))
    )

    DISPLAYSURF.blit(
        collected_text,
        collected_text.get_rect(center = (SCREEN_WIDTH // 2, 380))
    )

    DISPLAYSURF.blit(
        passed_text,
        passed_text.get_rect(center = (SCREEN_WIDTH // 2, 410))
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
C1 = Coin()

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    P1.update()
    E1.move()
    C1.move()


    if P1.rect.colliderect(E1.rect):
        game_over()

    if P1.rect.colliderect(C1.rect):
        collected_coins += C1.value
        C1.reset_position()

    if collected_coins >= level *10:
        enemy_speed += 3
        level += 1

    DISPLAYSURF.blit(background, (0, 0))
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    C1.draw(DISPLAYSURF)
    show_info()
    show_coins()
    show_level()

    pygame.display.update()
    FramePerSec.tick(FPS)