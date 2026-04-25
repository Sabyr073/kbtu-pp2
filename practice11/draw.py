import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 18)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
YELLOW = (255, 215, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)

# Canvas for drawing
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# -----------------------------
# TOOL SETTINGS
# -----------------------------
tool = "brush"
color = BLACK
brush_size = 6
drawing = False
start_pos = None
last_pos = None

colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE]
color_rects = []

# Create palette rectangles
for i, c in enumerate(colors):
    rect = pygame.Rect(10 + i * 50, 10, 40, 40)
    color_rects.append((rect, c))


# -----------------------------
# DRAW UI
# -----------------------------
def draw_ui():
    # Draw canvas
    screen.blit(canvas, (0, 0))

    # Draw top panel
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 110))

    # Draw color palette
    for rect, c in color_rects:
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # Draw current tool
    tool_text = font.render(f"Tool: {tool}", True, BLACK)

    # Draw first line of tool keys
    keys_text1 = font.render(
        "B Brush | R Rect | C Circle | E Eraser",
        True,
        BLACK
    )

    # Draw second line of tool keys
    keys_text2 = font.render(
        "S Square | T RightTri | Q EqTri | H Rhombus",
        True,
        BLACK
    )

    screen.blit(tool_text, (430, 10))
    screen.blit(keys_text1, (430, 40))
    screen.blit(keys_text2, (430, 70))


# -----------------------------
# DRAW SHAPES
# -----------------------------
def draw_square(start, end):
    # Draw square using the smaller side
    x1, y1 = start
    x2, y2 = end

    size = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x1 -= size
    if y2 < y1:
        y1 -= size

    rect = pygame.Rect(x1, y1, size, size)
    pygame.draw.rect(canvas, color, rect, 3)


def draw_right_triangle(start, end):
    # Draw right triangle from start and end points
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(canvas, color, points, 3)


def draw_equilateral_triangle(start, end):
    # Draw equilateral triangle using side length
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)
    height = int(side * math.sqrt(3) / 2)

    points = [
        (x1, y1),
        (x1 + side, y1),
        (x1 + side // 2, y1 - height)
    ]

    pygame.draw.polygon(canvas, color, points, 3)


def draw_rhombus(start, end):
    # Draw rhombus using center and mouse position
    x1, y1 = start
    x2, y2 = end

    width = abs(x2 - x1)
    height = abs(y2 - y1)

    center_x = x1
    center_y = y1

    points = [
        (center_x, center_y - height),
        (center_x + width, center_y),
        (center_x, center_y + height),
        (center_x - width, center_y)
    ]

    pygame.draw.polygon(canvas, color, points, 3)


# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Change tool with keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_s:
                tool = "square"
            elif event.key == pygame.K_t:
                tool = "right triangle"
            elif event.key == pygame.K_q:
                tool = "equilateral triangle"
            elif event.key == pygame.K_h:
                tool = "rhombus"

        # Start drawing
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Check color palette click
            clicked_color = False
            for rect, c in color_rects:
                if rect.collidepoint(mx, my):
                    color = c
                    clicked_color = True
                    break

            # Start drawing only under top panel
            if not clicked_color and my > 110:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

                # Draw brush dot
                if tool == "brush":
                    pygame.draw.circle(canvas, color, event.pos, brush_size)

                # Draw eraser dot
                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, event.pos, 20)

        # Draw while mouse is moving
        if event.type == pygame.MOUSEMOTION and drawing:
            # Brush drawing
            if tool == "brush":
                pygame.draw.line(canvas, color, last_pos, event.pos, brush_size * 2)
                last_pos = event.pos

            # Eraser drawing
            elif tool == "eraser":
                pygame.draw.line(canvas, WHITE, last_pos, event.pos, 30)
                last_pos = event.pos

        # Finish drawing shape
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            drawing = False
            end_pos = event.pos

            # Draw rectangle
            if tool == "rect":
                x1, y1 = start_pos
                x2, y2 = end_pos

                rect = pygame.Rect(
                    min(x1, x2),
                    min(y1, y2),
                    abs(x2 - x1),
                    abs(y2 - y1)
                )

                pygame.draw.rect(canvas, color, rect, 3)

            # Draw circle
            elif tool == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos

                radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(canvas, color, start_pos, radius, 3)

            # Draw square
            elif tool == "square":
                draw_square(start_pos, end_pos)

            # Draw right triangle
            elif tool == "right triangle":
                draw_right_triangle(start_pos, end_pos)

            # Draw equilateral triangle
            elif tool == "equilateral triangle":
                draw_equilateral_triangle(start_pos, end_pos)

            # Draw rhombus
            elif tool == "rhombus":
                draw_rhombus(start_pos, end_pos)

    # Update screen
    draw_ui()
    pygame.display.update()
    clock.tick(60)