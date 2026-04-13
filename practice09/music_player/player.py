import pygame

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600,200))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 32)

playlist = [
    "music/alexgrohl-sweet-life-luxury-chill-438146.mp3",
    "music/chill_background-the-weekend-117427.mp3",
    "music/ummbrella-deep-abstract-ambient_snowcap-401656.mp3"
]

current_track = 0

def play_music():
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s:
                play_music()

            elif event.key == pygame.K_w:
                pygame.mixer.music.stop()

            elif event.key == pygame.K_d:
                current_track = (current_track + 1) % len(playlist)
                play_music()

            elif event.key == pygame.K_a:
                current_track = (current_track - 1) % len(playlist)
                play_music()

            elif event.key == pygame.K_q:
                running = False

    screen.fill((30,30,30))

    text = font.render(
        f"Track: {current_track+1}",
        True,
        (255,255,255)
    )

    screen.blit(text,(20,80))

    pygame.display.update()

pygame.quit()