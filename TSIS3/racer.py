import pygame
import random
import time
from persistence import add_score

pygame.mixer.init()

WIDTH = 500
HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)   
GRAY = (90, 90, 90)
RED = (220, 0, 0)
BLUE = (0, 0, 220)
GREEN = (0, 180, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (130, 0, 130)
CYAN = (0, 200, 255)

LANES = [100, 200, 300, 400]

# -----------------------------
# LOAD ASSETS
# -----------------------------
background_img = pygame.image.load("assets/AnimatedStreet.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

player_img = pygame.image.load("assets/Player.png")
player_img = pygame.transform.scale(player_img, (50, 90))

enemy_img = pygame.image.load("assets/Enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 90))

nitro_img = pygame.image.load("assets/nitro.png")
nitro_img = pygame.transform.scale(nitro_img, (70, 60))

coin_img = pygame.image.load("assets/coins.png")
coin_img = pygame.transform.scale(coin_img, (70, 60))

shield_img = pygame.image.load("assets/shield.png")
shield_img = pygame.transform.scale(shield_img, (70, 60))

repair_img = pygame.image.load("assets/repair.png")
repair_img = pygame.transform.scale(repair_img, (50, 40))

crash_sound = pygame.mixer.Sound("assets/crash.wav")

pygame.mixer.music.load("assets/background.wav")


class Player:
    def __init__(self, color):
        self.rect = pygame.Rect(225, 580, 50, 90)
        self.color = color
        self.shield = False
        self.nitro_until = 0

    def move(self, keys):
        speed = 7

        if time.time() < self.nitro_until:
            speed = 12

        if keys[pygame.K_LEFT] and self.rect.left > 40:
            self.rect.x -= speed

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 40:
            self.rect.x += speed

    def draw(self, screen):
        screen.blit(player_img, self.rect)

        if self.shield:
            pygame.draw.rect(screen, CYAN, self.rect.inflate(10, 10), 3)


class FallingObject:
    def __init__(self, kind, y, speed):
        self.kind = kind
        self.speed = speed
        self.value = 1

        lane_x = random.choice(LANES)
        self.rect = pygame.Rect(lane_x - 25, y, 50, 50)

        if kind == "coin":
            self.value = random.choice([1, 2, 3])
            size = 25 + self.value * 5
            self.rect.size = (size, size)

        elif kind == "traffic":
            self.rect.size = (50, 90)

        elif kind == "barrier":
            self.rect.size = (70, 30)

        elif kind == "oil":
            self.rect.size = (60, 35)

        elif kind in ["nitro", "shield", "repair"]:
            self.rect.size = (40, 40)

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        if self.kind == "coin":
            screen.blit(coin_img, self.rect)

        elif self.kind == "traffic":
            screen.blit(enemy_img, self.rect)

        elif self.kind == "barrier":
            pygame.draw.rect(screen, ORANGE, self.rect)

        elif self.kind == "oil":
            pygame.draw.ellipse(screen, BLACK, self.rect)

        elif self.kind == "nitro":
            screen.blit(nitro_img, self.rect)

        elif self.kind == "shield":
            screen.blit(shield_img, self.rect)

        elif self.kind == "repair":
            screen.blit(repair_img, self.rect)

def color_from_setting(name):
    if name == "red":
        return RED
    if name == "green":
        return GREEN
    return BLUE


def difficulty_speed(difficulty):
    if difficulty == "easy":
        return 5
    if difficulty == "hard":
        return 9
    return 7


def run_game(screen, font, username, settings):
    clock = pygame.time.Clock()

    player = Player(color_from_setting(settings["car_color"]))
    base_speed = difficulty_speed(settings["difficulty"])

    if settings["sound"]:
        pygame.mixer.music.play(-1)

    objects = []

    coins = 0
    score = 0
    distance = 0
    finish_distance = 10000

    active_power = None
    power_end_time = 0

    spawn_timer = 0
    power_timer = 0

    while True:
        dt = clock.tick(60)
        spawn_timer += dt
        power_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()
        player.move(keys)

        distance += 1
        score = coins * 10 + distance

        difficulty_bonus = distance // 200
        current_speed = base_speed + difficulty_bonus

        # Spawn traffic, obstacles and coins
        if spawn_timer > max(350, 900 - difficulty_bonus * 80):
            spawn_timer = 0

            kind = random.choice([
                "traffic",
                "traffic",
                "barrier",
                "oil",
                "coin",
                "coin",
                "coin"
            ])

            obj = FallingObject(kind, -100, current_speed)

            # Safe spawn logic: do not spawn too close to player
            if abs(obj.rect.centerx - player.rect.centerx) > 40 or obj.rect.y < 100:
                objects.append(obj)

        # Spawn power-ups every few seconds
        if power_timer > 5000:
            power_timer = 0
            kind = random.choice(["nitro", "shield", "repair"])
            objects.append(FallingObject(kind, -80, current_speed))

        # Draw road background
        screen.blit(background_img, (0, 0))

        for obj in objects[:]:
            obj.move()
            obj.draw(screen)

            if obj.rect.top > HEIGHT:
                objects.remove(obj)
                continue

            if player.rect.colliderect(obj.rect):

                if obj.kind == "coin":
                    coins += obj.value
                    objects.remove(obj)

                elif obj.kind in ["traffic", "barrier", "oil"]:
                    if player.shield:
                        player.shield = False
                        objects.remove(obj)
                    else:
                        if settings["sound"]:
                            crash_sound.play()
                            pygame.mixer.music.stop()

                        add_score(username, score, distance)

                        return {
                            "score": score,
                            "coins": coins,
                            "distance": distance
                        }

                elif obj.kind == "nitro":
                    active_power = "Nitro"
                    power_end_time = time.time() + 4
                    player.nitro_until = power_end_time
                    objects.remove(obj)

                elif obj.kind == "shield":
                    active_power = "Shield"
                    power_end_time = 0
                    player.shield = True
                    objects.remove(obj)

                elif obj.kind == "repair":
                    active_power = "Repair"
                    objects.clear()

        if active_power == "Nitro" and time.time() > power_end_time:
            active_power = None

        player.draw(screen)

        remaining = max(0, finish_distance - distance)

        info1 = font.render(f"Name: {username}", True, WHITE)
        info2 = font.render(f"Coins: {coins}", True, WHITE)
        info3 = font.render(f"Score: {score}", True, WHITE)
        info4 = font.render(f"Distance: {distance}/{finish_distance}", True, WHITE)
        info5 = font.render(f"Power: {active_power if active_power else 'None'}", True, WHITE)
        info6 = font.render(f"Remaining: {remaining}", True, WHITE)

        screen.blit(info1, (10, 10))
        screen.blit(info2, (10, 35))
        screen.blit(info3, (10, 60))
        screen.blit(info4, (10, 85))
        screen.blit(info5, (10, 110))
        screen.blit(info6, (10, 135))

        pygame.display.update()

        if distance >= finish_distance:
            if settings["sound"]:
                pygame.mixer.music.stop()

            add_score(username, score + 500, distance)

            return {
                "score": score + 500,
                "coins": coins,
                "distance": distance
            }