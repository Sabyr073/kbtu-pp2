import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surface = font.render(self.text, True, BLACK)
        screen.blit(
            text_surface,
            text_surface.get_rect(center=self.rect.center)
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)