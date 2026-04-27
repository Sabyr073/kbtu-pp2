import pygame
import sys

from ui import Button
from racer import run_game, WIDTH, HEIGHT
from persistence import load_settings, save_settings, load_leaderboard

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")

font = pygame.font.SysFont("Verdana", 22)
big_font = pygame.font.SysFont("Verdana", 42)

WHITE = (255, 255, 255)
GRAY = (70, 70, 70)

settings = load_settings()


def ask_username():
    name = ""

    while True:
        screen.fill(GRAY)

        title = big_font.render("Enter username", True, WHITE)
        text = font.render(name + "|", True, WHITE)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 220)))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, 300)))

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
    buttons = [
        Button(150, 220, 200, 50, "Play"),
        Button(150, 290, 200, 50, "Leaderboard"),
        Button(150, 360, 200, 50, "Settings"),
        Button(150, 430, 200, 50, "Quit")
    ]

    while True:
        screen.fill(GRAY)

        title = big_font.render("TSIS3 RACER", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

        for button in buttons:
            button.draw(screen, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if buttons[0].is_clicked(pos):
                    username = ask_username()
                    result = run_game(screen, font, username, settings)

                    if result == "quit":
                        pygame.quit()
                        sys.exit()

                    game_over_screen(result)

                elif buttons[1].is_clicked(pos):
                    leaderboard_screen()

                elif buttons[2].is_clicked(pos):
                    settings_screen()

                elif buttons[3].is_clicked(pos):
                    pygame.quit()
                    sys.exit()


def leaderboard_screen():
    back_button = Button(150, 600, 200, 50, "Back")

    small_font = pygame.font.SysFont("Verdana", 18)

    while True:
        screen.fill(GRAY)

        title = big_font.render("Leaderboard", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))

        scores = load_leaderboard()

        y = 130

        for i, item in enumerate(scores, start=1):
            rank_text = small_font.render(f"{i}.", True, WHITE)
            name_text = small_font.render(item["name"], True, WHITE)
            score_text = small_font.render(f"Score: {item['score']}", True, WHITE)
            distance_text = small_font.render(f"Dist: {item['distance']}", True, WHITE)

            screen.blit(rank_text, (35, y))
            screen.blit(name_text, (70, y))
            screen.blit(score_text, (210, y))
            screen.blit(distance_text, (360, y))

            y += 35

        back_button.draw(screen, font)
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

    sound_button = Button(120, 240, 260, 45, "Change Sound")
    color_button = Button(120, 310, 260, 45, "Change Car Color")
    difficulty_button = Button(120, 380, 260, 45, "Change Difficulty")
    back_button = Button(120, 520, 260, 45, "Back")

    colors = ["blue", "red", "green"]
    difficulties = ["easy", "normal", "hard"]

    if "sound" not in settings:
        settings["sound"] = True
    if "car_color" not in settings:
        settings["car_color"] = "blue"
    if "difficulty" not in settings:
        settings["difficulty"] = "normal"

    while True:
        screen.fill(GRAY)

        title = big_font.render("Settings", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        sound_text = font.render(f"Sound: {settings['sound']}", True, WHITE)
        color_text = font.render(f"Car color: {settings['car_color']}", True, WHITE)
        difficulty_text = font.render(f"Difficulty: {settings['difficulty']}", True, WHITE)

        screen.blit(sound_text, (130, 120))
        screen.blit(color_text, (130, 150))
        screen.blit(difficulty_text, (130, 180))

        sound_button.draw(screen, font)
        color_button.draw(screen, font)
        difficulty_button.draw(screen, font)
        back_button.draw(screen, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button.is_clicked(event.pos):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                elif color_button.is_clicked(event.pos):
                    index = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(index + 1) % len(colors)]
                    save_settings(settings)

                elif difficulty_button.is_clicked(event.pos):
                    index = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                    save_settings(settings)

                elif back_button.is_clicked(event.pos):
                    return


def game_over_screen(result):
    retry_button = Button(150, 420, 200, 50, "Retry")
    menu_button = Button(150, 490, 200, 50, "Main Menu")

    while True:
        screen.fill(GRAY)

        title = big_font.render("GAME OVER", True, WHITE)
        score = font.render(f"Score: {result['score']}", True, WHITE)
        coins = font.render(f"Coins: {result['coins']}", True, WHITE)
        distance = font.render(f"Distance: {result['distance']}", True, WHITE)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, 140)))
        screen.blit(score, score.get_rect(center=(WIDTH // 2, 230)))
        screen.blit(coins, coins.get_rect(center=(WIDTH // 2, 270)))
        screen.blit(distance, distance.get_rect(center=(WIDTH // 2, 310)))

        retry_button.draw(screen, font)
        menu_button.draw(screen, font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.is_clicked(event.pos):
                    username = ask_username()
                    result = run_game(screen, font, username, settings)

                elif menu_button.is_clicked(event.pos):
                    return


main_menu()