import pygame
import random

CELL = 20
GRID_W = 25
GRID_H = 25

WIDTH = CELL * GRID_W
HEIGHT = CELL * GRID_H

WHITE = (255, 255, 255)
GRAY = (210, 210, 210)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
DARK_RED = (120, 0, 0)
BLUE = (0, 0, 220)
PURPLE = (140, 0, 140)
CYAN = (0, 200, 255)
ORANGE = (255, 140, 0)

# -----------------------------
# LOAD ASSETS
# -----------------------------
pygame.mixer.init()

speed_img = pygame.image.load("assets/speed.png")
speed_img = pygame.transform.scale(speed_img, (CELL, CELL))

slow_img = pygame.image.load("assets/slow.png")
slow_img = pygame.transform.scale(slow_img, (CELL, CELL))

shield_img = pygame.image.load("assets/shield.png")
shield_img = pygame.transform.scale(shield_img, (30, 30))

pygame.mixer.music.load("assets/music.mp3")


def random_free_cell(snake, walls, food=None, poison=None, bonus=None):
    while True:
        pos = (
            random.randint(0, GRID_W - 1),
            random.randint(0, GRID_H - 1)
        )

        if pos in snake:
            continue
        if pos in walls:
            continue
        if pos == food:
            continue
        if pos == poison:
            continue
        if pos == bonus:
            continue

        return pos


def stop_music(settings):
    if settings["sound"]:
        pygame.mixer.music.stop()


def find_safe_direction(snake, walls, current_direction):
    head_x, head_y = snake[0]

    directions = [
        current_direction,
        (1, 0),    # right
        (-1, 0),   # left
        (0, -1),   # up
        (0, 1)     # down
    ]

    for dx, dy in directions:
        new_pos = (head_x + dx, head_y + dy)

        if new_pos[0] < 0 or new_pos[0] >= GRID_W:
            continue
        if new_pos[1] < 0 or new_pos[1] >= GRID_H:
            continue
        if new_pos in snake:
            continue
        if new_pos in walls:
            continue

        return (dx, dy), new_pos

    return None, snake[0]

def run_snake(screen, font, username, settings, personal_best):
    clock = pygame.time.Clock()

    if settings["sound"]:
        pygame.mixer.music.play(-1)

    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    next_direction = (1, 0)

    score = 0
    level = 1
    base_speed = 6

    walls = set()

    food = random_free_cell(snake, walls)
    food_value = random.choice([1, 2, 3])
    food_spawn_time = pygame.time.get_ticks()
    food_lifetime = 5000

    poison = random_free_cell(snake, walls, food=food)

    bonus = None
    bonus_type = None
    bonus_spawn_time = 0
    bonus_lifetime = 8000

    active_bonus = None
    active_bonus_end = 0
    shield = False

    while True:
        now = pygame.time.get_ticks()

        # Speed depends on level and active bonus
        speed = base_speed + level

        if active_bonus == "speed" and now < active_bonus_end:
            speed += 4

        elif active_bonus == "slow" and now < active_bonus_end:
            speed = max(3, speed - 3)

        if active_bonus in ["speed", "slow"] and now >= active_bonus_end:
            active_bonus = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music(settings)
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)

                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)

                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)

                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        direction = next_direction

        # Food disappears after timer
        if now - food_spawn_time > food_lifetime:
            food = random_free_cell(snake, walls, poison=poison, bonus=bonus)
            food_value = random.choice([1, 2, 3])
            food_spawn_time = now

        # Spawn one temporary bonus
        if bonus is None and random.randint(1, 120) == 1:
            bonus_type = random.choice(["speed", "slow", "shield"])
            bonus = random_free_cell(snake, walls, food=food, poison=poison)
            bonus_spawn_time = now

        # Bonus disappears after 8 seconds
        if bonus is not None and now - bonus_spawn_time > bonus_lifetime:
            bonus = None
            bonus_type = None

        # Move snake
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        collision = (
            new_head[0] < 0 or new_head[0] >= GRID_W or
            new_head[1] < 0 or new_head[1] >= GRID_H or
            new_head in snake or
            new_head in walls
        )

        # Shield ignores one collision
        if collision:
            if shield:
                shield = False
                active_bonus = None

                safe_direction, safe_head = find_safe_direction(
                    snake,
                    walls,
                    direction
                )

                if safe_direction is not None:
                    direction = safe_direction
                    next_direction = safe_direction
                    new_head = safe_head
                else:
                    stop_music(settings)
                    return {
                        "score": score,
                        "level": level,
                        "personal_best": personal_best
                    }
            else:
                stop_music(settings)
                return {
                    "score": score,
                    "level": level,
                    "personal_best": personal_best
                }

        snake.insert(0, new_head)

        # Normal weighted food
        if new_head == food:
            score += food_value

            food_value = random.choice([1, 2, 3])
            food = random_free_cell(snake, walls, poison=poison, bonus=bonus)
            food_spawn_time = now

            if score >= level * 5:
                level += 1

                # From level 3, random wall blocks appear
                if level >= 3:
                    for _ in range(level):
                        wall = random_free_cell(
                            snake,
                            walls,
                            food=food,
                            poison=poison,
                            bonus=bonus
                        )
                        walls.add(wall)

        # Poison food shortens snake
        elif new_head == poison:
            poison = random_free_cell(snake, walls, food=food, bonus=bonus)

            for _ in range(2):
                if len(snake) > 1:
                    snake.pop()

            if len(snake) <= 1:
                stop_music(settings)
                return {
                    "score": score,
                    "level": level,
                    "personal_best": personal_best
                }

        # Bonus pickup
        elif bonus is not None and new_head == bonus:
            if bonus_type == "speed":
                active_bonus = "speed"
                active_bonus_end = now + 5000

            elif bonus_type == "slow":
                active_bonus = "slow"
                active_bonus_end = now + 5000

            elif bonus_type == "shield":
                active_bonus = "shield"
                shield = True

            bonus = None
            bonus_type = None

            snake.pop()

        else:
            snake.pop()

        # -----------------------------
        # DRAW
        # -----------------------------
        screen.fill(WHITE)

        if settings["grid"]:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # Walls
        for wall in walls:
            pygame.draw.rect(
                screen,
                BLACK,
                (wall[0] * CELL, wall[1] * CELL, CELL, CELL)
            )

        # Food color depends on value
        if food_value == 1:
            food_color = RED
        elif food_value == 2:
            food_color = BLUE
        else:
            food_color = PURPLE

        pygame.draw.rect(
            screen,
            food_color,
            (food[0] * CELL, food[1] * CELL, CELL, CELL)
        )

        # Poison food
        pygame.draw.rect(
            screen,
            DARK_RED,
            (poison[0] * CELL, poison[1] * CELL, CELL, CELL)
        )

        # Bonus icons
        if bonus is not None:
            bonus_rect = pygame.Rect(
                bonus[0] * CELL,
                bonus[1] * CELL,
                CELL,
                CELL
            )

            if bonus_type == "speed":
                screen.blit(speed_img, bonus_rect)

            elif bonus_type == "slow":
                screen.blit(slow_img, bonus_rect)

            elif bonus_type == "shield":
                screen.blit(shield_img, bonus_rect)

        # Snake
        snake_color = tuple(settings["snake_color"])

        for i, part in enumerate(snake):
            if i == 0:
                color = snake_color
            else:
                color = (0, 120, 0)

            pygame.draw.rect(
                screen,
                color,
                (part[0] * CELL, part[1] * CELL, CELL, CELL)
            )

        # If shield active, draw outline around snake head
        if shield:
            head = snake[0]
            pygame.draw.rect(
                screen,
                CYAN,
                (head[0] * CELL, head[1] * CELL, CELL, CELL),
                3
            )

        info = [
            f"Player: {username}",
            f"Score: {score}",
            f"Level: {level}",
            f"Best: {personal_best}",
            f"Food: +{food_value}",
            f"Bonus: {active_bonus if active_bonus else 'None'}"
        ]

        y = 5
        for line in info:
            text = font.render(line, True, BLACK)
            screen.blit(text, (5, y))
            y += 22

        pygame.display.update()
        clock.tick(speed)