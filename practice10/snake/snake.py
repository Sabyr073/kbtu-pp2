import pygame
import random
import sys

pygame.init()

# -----------------------------
# SETTINGS
# -----------------------------
CELL = 20
GRID_W = 15
GRID_H = 20

WIDTH = CELL * GRID_W      # 300
HEIGHT = CELL * GRID_H     # 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 18)

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)

# -----------------------------
# GAME VARIABLES
# -----------------------------
# start near top-left corner
snake = [(3, 2), (2, 2), (1, 2)]

direction = (1, 0)
next_direction = (1, 0)

score = 0
level = 1
speed = 3

walls = set()
food = None


# -----------------------------
# LOAD LEVEL FROM TXT
# -----------------------------
def load_level(level_number):
    global walls

    walls = set()
    filename = f"level{level_number}.txt"

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            line = line.strip()
            for x, char in enumerate(line):
                if char == "#":
                    walls.add((x, y))

    except FileNotFoundError:
        print(f"{filename} not found")
        pygame.quit()
        sys.exit()


# -----------------------------
# GENERATE FOOD
# -----------------------------
def generate_food():
    while True:
        pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if pos not in snake and pos not in walls:
            return pos


# -----------------------------
# DRAW ONE CELL
# -----------------------------
def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))


# -----------------------------
# DRAW CHESS BACKGROUND
# -----------------------------
def draw_background():
    for y in range(GRID_H):
        for x in range(GRID_W):
            if (x + y) % 2 == 0:
                color = WHITE
            else:
                color = GRAY

            pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))


# -----------------------------
# DRAW EVERYTHING
# -----------------------------
def draw_game():
    draw_background()

    # draw walls
    for wall in walls:
        draw_cell(wall, BLACK)

    # draw snake
    for i, part in enumerate(snake):
        if i == 0:
            draw_cell(part, GREEN)
        else:
            draw_cell(part, DARK_GREEN)

    # draw food
    draw_cell(food, RED)

    # draw score and level
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (200, 10))

    pygame.display.update()


# -----------------------------
# GAME OVER SCREEN
# -----------------------------
def game_over():
    screen.fill(WHITE)

    text1 = font.render("GAME OVER", True, RED)
    text2 = font.render(f"Score: {score}", True, BLACK)
    text3 = font.render(f"Level: {level}", True, BLACK)

    screen.blit(text1, text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
    screen.blit(text2, text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
    screen.blit(text3, text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35)))

    pygame.display.update()
    pygame.time.delay(2500)
    pygame.quit()
    sys.exit()


# -----------------------------
# NEXT LEVEL
# -----------------------------
def next_level():
    global level, speed, food

    level += 1
    speed += 3

    # load new walls
    load_level(level)

    # if snake appears inside wall after loading new level -> game over
    for part in snake:
        if part in walls:
            game_over()

    # generate new food
    food = generate_food()


# -----------------------------
# START FIRST LEVEL
# -----------------------------
load_level(level)

# if snake starts inside wall, stop immediately
for part in snake:
    if part in walls:
        print("Snake starts inside a wall. Fix level1.txt")
        pygame.quit()
        sys.exit()

food = generate_food()

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

    # move snake
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # check wall collision
    if new_head in walls:
        game_over()

    # check out of screen
    if new_head[0] < 0 or new_head[0] >= GRID_W or new_head[1] < 0 or new_head[1] >= GRID_H:
        game_over()

    # check self collision
    if new_head in snake:
        game_over()

    snake.insert(0, new_head)

    # check food
    if new_head == food:
        score += 1
        food = generate_food()

        # every 3 points -> next level
        if score % 3 == 0:
            next_level()
    else:
        snake.pop()

    draw_game()
    clock.tick(speed)