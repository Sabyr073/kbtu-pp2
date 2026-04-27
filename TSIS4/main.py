import pygame
import sys
import json

from game import run_snake, WIDTH, HEIGHT
from db import create_tables, save_result, get_top_scores, get_personal_best


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake")

font = pygame.font.SysFont("Verdana", 18)
big_font = pygame.font.SysFont("Verdana", 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)


SETTINGS_FILE = "settings.json"


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        settings = {
            "snake_color": [0, 180, 0],
            "grid": True,
            "sound": True
        }
        save_settings(settings)
        return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


settings = load_settings()


def ask_username():
    name = ""

    while True:
        screen.fill(DARK_GRAY)

        title = big_font.render("Enter username", True, WHITE)
        text = font.render(name + "|", True, WHITE)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, 260)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    name += event.unicode


def main_menu():
    play_button = Button(150, 160, 200, 45, "Play")
    leaderboard_button = Button(150, 220, 200, 45, "Leaderboard")
    settings_button = Button(150, 280, 200, 45, "Settings")
    quit_button = Button(150, 340, 200, 45, "Quit")

    while True:
        screen.fill(DARK_GRAY)

        title = big_font.render("TSIS4 SNAKE", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        play_button.draw()
        leaderboard_button.draw()
        settings_button.draw()
        quit_button.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if play_button.is_clicked(pos):
                    username = ask_username()
                    personal_best = get_personal_best(username)

                    result = run_snake(
                        screen,
                        font,
                        username,
                        settings,
                        personal_best
                    )

                    if result == "quit":
                        pygame.quit()
                        sys.exit()

                    save_result(username, result["score"], result["level"])
                    game_over_screen(username, result)

                elif leaderboard_button.is_clicked(pos):
                    leaderboard_screen()

                elif settings_button.is_clicked(pos):
                    settings_screen()

                elif quit_button.is_clicked(pos):
                    pygame.quit()
                    sys.exit()


def leaderboard_screen():
    back_button = Button(150, HEIGHT - 70, 200, 45, "Back")

    while True:
        screen.fill(DARK_GRAY)

        title = big_font.render("Leaderboard", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 50)))

        scores = get_top_scores()

        y = 100

        if not scores:
            empty_text = font.render("No scores yet", True, WHITE)
            screen.blit(empty_text, empty_text.get_rect(center=(WIDTH // 2, 150)))
        else:
            for i, row in enumerate(scores, start=1):
                username, score, level, played_at = row

                line = font.render(
                    f"{i}. {username} | Score: {score} | Level: {level}",
                    True,
                    WHITE
                )

                date_line = font.render(
                    f"Date: {str(played_at)[:19]}",
                    True,
                    WHITE
                )

                screen.blit(line, (25, y))
                screen.blit(date_line, (25, y + 22))
                y += 50

        back_button.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    return


def settings_screen():
    global settings

    grid_button = Button(120, 190, 260, 45, "Change Grid")
    sound_button = Button(120, 250, 260, 45, "Change Sound")
    color_button = Button(120, 310, 260, 45, "Change Snake Color")
    save_button = Button(120, 400, 260, 45, "Back")

    colors = [
        [0, 180, 0],
        [0, 0, 220],
        [220, 0, 0],
        [128, 0, 128]
    ]

    while True:
        screen.fill(DARK_GRAY)

        title = big_font.render("Settings", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        grid_text = font.render(f"Grid: {settings['grid']}", True, WHITE)
        sound_text = font.render(f"Sound: {settings['sound']}", True, WHITE)
        color_text = font.render(f"Snake color: {settings['snake_color']}", True, WHITE)

        screen.blit(grid_text, (95, 110))
        screen.blit(sound_text, (95, 135))
        screen.blit(color_text, (95, 160))

        grid_button.draw()
        sound_button.draw()
        color_button.draw()
        save_button.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_button.is_clicked(event.pos):
                    settings["grid"] = not settings["grid"]

                elif sound_button.is_clicked(event.pos):
                    settings["sound"] = not settings["sound"]

                elif color_button.is_clicked(event.pos):
                    current = settings["snake_color"]

                    if current not in colors:
                        settings["snake_color"] = colors[0]
                    else:
                        index = colors.index(current)
                        settings["snake_color"] = colors[(index + 1) % len(colors)]

                elif save_button.is_clicked(event.pos):
                    save_settings(settings)
                    return


def game_over_screen(username, result):
    retry_button = Button(150, 300, 200, 45, "Retry")
    menu_button = Button(150, 360, 200, 45, "Main Menu")

    while True:
        screen.fill(DARK_GRAY)

        title = big_font.render("GAME OVER", True, WHITE)

        score_text = font.render(f"Score: {result['score']}", True, WHITE)
        level_text = font.render(f"Level: {result['level']}", True, WHITE)
        best_text = font.render(
            f"Personal best: {max(result['personal_best'], result['score'])}",
            True,
            WHITE
        )

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 90)))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, 150)))
        screen.blit(level_text, level_text.get_rect(center=(WIDTH // 2, 180)))
        screen.blit(best_text, best_text.get_rect(center=(WIDTH // 2, 210)))

        retry_button.draw()
        menu_button.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.is_clicked(event.pos):
                    personal_best = get_personal_best(username)

                    result = run_snake(
                        screen,
                        font,
                        username,
                        settings,
                        personal_best
                    )

                    if result == "quit":
                        pygame.quit()
                        sys.exit()

                    save_result(username, result["score"], result["level"])

                elif menu_button.is_clicked(event.pos):
                    return


create_tables()
main_menu()