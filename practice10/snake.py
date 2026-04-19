import pygame
import random
import sys

pygame.init()

# -----------------------------
# SETTINGS
# -----------------------------
CELL = 20
GRID_W = 30
GRID_H = 20

WIDTH = CELL * GRID_W
HEIGHT = CELL * GRID_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
GRAY = (120, 120, 120)

# -----------------------------
# WALLS
# -----------------------------
walls = set()

# Border walls
for x in range(GRID_W):
    walls.add((x, 0))
    walls.add((x, GRID_H - 1))

for y in range(GRID_H):
    walls.add((0, y))
    walls.add((GRID_W - 1, y))

# Some internal walls
for x in range(8, 12):
    walls.add((x, 6))
for x in range(16, 22):
    walls.add((x, 12))

# -----------------------------
# SNAKE
# -----------------------------
snake = [(5, 5), (4, 5), (3, 5)]
direction = (1, 0)
next_direction = (1, 0)

score = 0
level = 1
foods_for_next_level = 4
speed = 8

# -----------------------------
# FOOD
# -----------------------------
def generate_food():
    """
    Generate food in random position not occupied by snake or walls.
    """
    while True:
        pos = (random.randint(1, GRID_W - 2), random.randint(1, GRID_H - 2))
        if pos not in snake and pos not in walls:
            return pos

food = generate_food()

# -----------------------------
# DRAW HELPERS
# -----------------------------
def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))

def draw_game():
    screen.fill(BLACK)

    # Draw walls
    for wall in walls:
        draw_cell(wall, GRAY)

    # Draw snake
    for i, part in enumerate(snake):
        if i == 0:
            draw_cell(part, GREEN)
        else:
            draw_cell(part, DARK_GREEN)

    # Draw food
    draw_cell(food, RED)

    # Draw score and level
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 100, 10))

    pygame.display.update()

def game_over():
    screen.fill(BLACK)
    text1 = font.render("GAME OVER", True, RED)
    text2 = font.render(f"Score: {score}   Level: {level}", True, WHITE)

    screen.blit(text1, text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
    screen.blit(text2, text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
    pygame.display.update()
    pygame.time.delay(2500)
    pygame.quit()
    sys.exit()

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    # New head position
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # Check wall/border collision
    if new_head in walls:
        game_over()

    # Check self collision
    if new_head in snake:
        game_over()

    snake.insert(0, new_head)

    # Check food collision
    if new_head == food:
        score += 1
        food = generate_food()

        # Level up every 4 foods
        if score % foods_for_next_level == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    draw_game()
    clock.tick(speed)