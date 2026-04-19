import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 18)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
YELLOW = (255, 215, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)

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
    screen.blit(canvas, (0, 0))

    # Top panel
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 60))

    # Color palette
    for rect, c in color_rects:
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # Current tool text
    text = font.render(f"Tool: {tool} | Keys: B-brush R-rect C-circle E-eraser", True, BLACK)
    screen.blit(text, (350, 20))

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Check color palette
            clicked_color = False
            for rect, c in color_rects:
                if rect.collidepoint(mx, my):
                    color = c
                    clicked_color = True
                    break

            if not clicked_color and my > 60:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

                if tool == "brush":
                    pygame.draw.circle(canvas, color, event.pos, brush_size)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, event.pos, 20)

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "brush":
                pygame.draw.line(canvas, color, last_pos, event.pos, brush_size * 2)
                last_pos = event.pos
            elif tool == "eraser":
                pygame.draw.line(canvas, WHITE, last_pos, event.pos, 30)
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            drawing = False
            end_pos = event.pos

            if tool == "rect":
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                   abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(canvas, color, rect, 3)

            elif tool == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(canvas, color, start_pos, radius, 3)

    draw_ui()
    pygame.display.update()
    clock.tick(60)