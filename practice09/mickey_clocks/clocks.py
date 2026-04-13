import pygame
import datetime
import math

pygame.init()


WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")


clock = pygame.image.load("images/clock.png")
left_hand = pygame.image.load("images/left_hand.png")
right_hand = pygame.image.load("images/right_hand.png")


center = (WIDTH//2, HEIGHT//2)


clock_timer = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                running = False

    now = datetime.datetime.now()

    seconds = now.second
    minutes = now.minute

    second_angle = -seconds * 6
    minute_angle = -minutes * 6

    rotated_left = pygame.transform.rotate(left_hand, second_angle)
    rotated_right = pygame.transform.rotate(right_hand, minute_angle)

    left_rect = rotated_left.get_rect(center=center)
    right_rect = rotated_right.get_rect(center=center)

    screen.fill((255,255,255))

    clock_rect = clock.get_rect(center=center)

    screen.blit(clock, clock_rect)
    screen.blit(rotated_right, right_rect)
    screen.blit(rotated_left, left_rect)

    pygame.display.update()

    clock_timer.tick(60)

pygame.quit()