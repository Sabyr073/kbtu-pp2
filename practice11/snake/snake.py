import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Clock, speed, level and font
clock = pygame.time.Clock()
speed = 5
level = 1
font = pygame.font.SysFont("Verdana", 24)

# Grid settings
CELL = 25
GRID_W = WIDTH // CELL
GRID_H = HEIGHT // CELL

# Colors
WHITE = (240, 240, 240)
GRAY = (200, 200, 200)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 180)

# Game variables
snake = [(5, 5), (4, 5), (3, 5)]
direction = (1, 0)
score = 0
food = None
walls = []


def draw_grid():
    # Draw checkerboard background
    for y in range(GRID_H):
        for x in range(GRID_W):
            if (x + y) % 2 == 0:
                color = WHITE
            else:
                color = GRAY

            pygame.draw.rect(
                screen,
                color,
                (x * CELL, y * CELL, CELL, CELL)
            )


def draw_cell(pos, color):
    # Draw one cell on the grid
    x, y = pos
    pygame.draw.rect(
        screen,
        color,
        (x * CELL, y * CELL, CELL, CELL)
    )


def draw_snake():
    # Draw snake head and body
    for i, part in enumerate(snake):
        if i == 0:
            draw_cell(part, GREEN)
        else:
            draw_cell(part, DARK_GREEN)


def move_snake():
    global food, score

    # Get current head position
    head_x, head_y = snake[0]
    dx, dy = direction

    # Create new head position
    new_head = (head_x + dx, head_y + dy)

    # Check screen border collision
    if new_head[0] < 0 or new_head[0] >= GRID_W or new_head[1] < 0 or new_head[1] >= GRID_H:
        game_over()

    # Check self collision
    if new_head in snake:
        game_over()

    # Check wall collision
    if new_head in walls:
        game_over()

    # Add new head
    snake.insert(0, new_head)

    # Check food collision
    if new_head == food["pos"]:
        score += food["value"]
        update_level()
        food = generate_food()
    else:
        snake.pop()


def game_over():
    # Show game over screen
    screen.fill(BLACK)

    font1 = pygame.font.SysFont("Verdana", 40)
    text = font1.render("GAME OVER", True, RED)

    level_text = font.render(f"Level: {level}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)

    screen.blit(
        text,
        text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    )

    screen.blit(
        level_text,
        level_text.get_rect(center=(WIDTH // 2, 285))
    )

    screen.blit(
        score_text,
        score_text.get_rect(center=(WIDTH // 2, 320))
    )

    pygame.display.flip()
    pygame.time.delay(2500)

    pygame.quit()
    sys.exit()


def load_level(level_number):
    global walls

    # Clear old walls
    walls = []

    filename = f"level{level_number}.txt"

    try:
        # Read level file
        with open(filename, "r") as file:
            lines = file.readlines()

        # Convert # symbols into wall positions
        for y, line in enumerate(lines):
            line = line.strip()

            for x, char in enumerate(line):
                if char == "#":
                    walls.append((x, y))

    except FileNotFoundError:
        print(f"{filename} not found")
        pygame.quit()
        sys.exit()


def draw_walls():
    # Draw all wall cells
    for wall in walls:
        draw_cell(wall, BLUE)


def generate_food():
    # Generate food outside snake and walls
    while True:
        food_pos = (
            random.randint(0, GRID_W - 1),
            random.randint(0, GRID_H - 1)
        )

        if food_pos not in snake and food_pos not in walls:
            return {
                "pos": food_pos,
                "value": random.randint(1, 3),
                "spawn_time": pygame.time.get_ticks(),
                "lifetime": 5000
            }


def draw_food():
    # Draw food and its value
    draw_cell(food["pos"], RED)

    value_text = font.render(str(food["value"]), True, BLACK)
    screen.blit(
        value_text,
        (food["pos"][0] * CELL + 3, food["pos"][1] * CELL - 6)
    )


def draw_info():
    # Draw score and level
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (130, 10))


def update_food_timer():
    global food

    # Check food lifetime
    current_time = pygame.time.get_ticks()

    if current_time - food["spawn_time"] >= food["lifetime"]:
        food = generate_food()


def update_level():
    global level, speed, food

    # Increase level and speed
    if score >= level * 5:
        level += 1
        speed += 2

        # Load next level if it exists
        if level <= 3:
            load_level(level)
            food = generate_food()


# Load first level
load_level(level)

# Create first food
food = generate_food()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle keyboard movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # Update game state
    update_food_timer()
    move_snake()

    # Draw everything
    draw_grid()
    draw_walls()
    draw_snake()
    draw_food()
    draw_info()

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()