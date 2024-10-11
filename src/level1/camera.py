import pygame
screen_width, screen_height = 800, 600

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width-10
        self.height = height-10

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(screen_width / 2)
        y = -target.rect.centery + int(screen_height / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - screen_width), x)  # Right
        y = max(-(self.height - screen_height), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)