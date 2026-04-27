import pygame
import sys
import math
from datetime import datetime
from collections import deque

pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 16)
text_font = pygame.font.SysFont("Arial", 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
YELLOW = (255, 215, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

tool = "pencil"
color = BLACK
brush_size = 2

drawing = False
start_pos = None
last_pos = None
preview_pos = None

text_active = False
text_position = None
text_value = ""

colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE]
color_rects = []

for i, c in enumerate(colors):
    rect = pygame.Rect(10 + i * 50, 10, 40, 40)
    color_rects.append((rect, c))


def to_canvas_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def inside_canvas(pos):
    x, y = pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def draw_ui():
    screen.fill(GRAY)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    for rect, c in color_rects:
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    line1 = "P-pencil L-line R-rect C-circle E-eraser S-square T-right Y-eq H-rhombus F-fill X-text"
    line2 = f"Tool: {tool} | Brush: {brush_size} | 1=small 2=medium 3=large | Ctrl+S=save"

    screen.blit(font.render(line1, True, BLACK), (320, 12))
    screen.blit(font.render(line2, True, BLACK), (320, 42))

    if text_active:
        info = font.render(f"Typing: {text_value}", True, BLACK)
        screen.blit(info, (320, 65))


def draw_square(surface, start, end):
    x1, y1 = start
    x2, y2 = end
    side = max(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        side = -side

    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(surface, color, rect, brush_size)


def draw_right_triangle(surface, start, end):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x2, y1), (x1, y2)]
    pygame.draw.polygon(surface, color, points, brush_size)


def draw_equilateral_triangle(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    base = x2 - x1
    height = int(abs(base) * math.sqrt(3) / 2)

    points = [
        (x1, y2),
        (x2, y2),
        ((x1 + x2) // 2, y2 - height)
    ]

    pygame.draw.polygon(surface, color, points, brush_size)


def draw_rhombus(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    points = [
        (cx, y1),
        (x2, cy),
        (cx, y2),
        (x1, cy)
    ]

    pygame.draw.polygon(surface, color, points, brush_size)


def draw_shape(surface, selected_tool, start, end):
    if selected_tool == "line":
        pygame.draw.line(surface, color, start, end, brush_size)

    elif selected_tool == "rect":
        x1, y1 = start
        x2, y2 = end
        rect = pygame.Rect(
            min(x1, x2),
            min(y1, y2),
            abs(x2 - x1),
            abs(y2 - y1)
        )
        pygame.draw.rect(surface, color, rect, brush_size)

    elif selected_tool == "circle":
        x1, y1 = start
        x2, y2 = end
        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        pygame.draw.circle(surface, color, start, radius, brush_size)

    elif selected_tool == "square":
        draw_square(surface, start, end)

    elif selected_tool == "right_triangle":
        draw_right_triangle(surface, start, end)

    elif selected_tool == "equilateral_triangle":
        draw_equilateral_triangle(surface, start, end)

    elif selected_tool == "rhombus":
        draw_rhombus(surface, start, end)


def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()
    x, y = start_pos

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


def save_canvas():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"painting_{timestamp}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved as {filename}")


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if event.key == pygame.K_s:
                    save_canvas()

            if text_active:
                if event.key == pygame.K_RETURN:
                    rendered = text_font.render(text_value, True, color)
                    canvas.blit(rendered, text_position)
                    text_active = False
                    text_value = ""
                    text_position = None

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_value = ""
                    text_position = None

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            else:
                if event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_t:
                    tool = "right_triangle"
                elif event.key == pygame.K_y:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_x:
                    tool = "text"

                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            clicked_color = False
            for rect, c in color_rects:
                if rect.collidepoint(mx, my):
                    color = c
                    clicked_color = True
                    break

            if clicked_color:
                continue

            if inside_canvas(event.pos):
                canvas_pos = to_canvas_pos(event.pos)

                if tool == "fill":
                    flood_fill(canvas, canvas_pos, color)

                elif tool == "text":
                    text_active = True
                    text_position = canvas_pos
                    text_value = ""

                else:
                    drawing = True
                    start_pos = canvas_pos
                    last_pos = canvas_pos
                    preview_pos = canvas_pos

                    if tool == "pencil":
                        pygame.draw.circle(canvas, color, canvas_pos, brush_size)

                    elif tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, canvas_pos, brush_size * 2)

        if event.type == pygame.MOUSEMOTION and drawing:
            if inside_canvas(event.pos):
                canvas_pos = to_canvas_pos(event.pos)
                preview_pos = canvas_pos

                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, canvas_pos, brush_size * 2)
                    last_pos = canvas_pos

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            drawing = False

            if inside_canvas(event.pos):
                end_pos = to_canvas_pos(event.pos)

                if tool not in ["pencil", "eraser"]:
                    draw_shape(canvas, tool, start_pos, end_pos)

            start_pos = None
            last_pos = None
            preview_pos = None

    draw_ui()

    if drawing and tool in [
        "line",
        "rect",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus"
    ] and start_pos and preview_pos:
        preview = canvas.copy()
        draw_shape(preview, tool, start_pos, preview_pos)
        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if text_active and text_position is not None:
        rendered = text_font.render(text_value, True, color)
        screen.blit(rendered, (text_position[0], text_position[1] + TOOLBAR_HEIGHT))

    pygame.display.update()
    clock.tick(60)