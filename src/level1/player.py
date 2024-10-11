import pygame
from PIL import Image, ImageSequence

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = self.load_gif(r"src\level1\player.gif") 
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.current_frame = 0
        self.animation_speed = 1  
        self.last_update = pygame.time.get_ticks()

    def load_gif(self, gif_path):
        pil_image = Image.open(gif_path)
        frames = []
        for frame in ImageSequence.Iterator(pil_image):
            frame = frame.convert("RGBA")
            pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frames.append(pygame_image)
        return frames
        
    def update(self, walls):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 * self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

     
        self.rect.x += self.speed_x
        self.collide(walls, 'x')

        # Move vertically
        self.rect.y += self.speed_y
        self.collide(walls, 'y')

    def move_left(self):
        self.speed_x = -(50 / 10)

    def move_right(self):
        self.speed_x = (50 / 10)

    def move_up(self):
        self.speed_y = -(50 / 10)

    def move_down(self):
        self.speed_y = (50 / 10)

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0

    def is_on_portal(self, portal):
        hits = pygame.sprite.spritecollide(self, portal, False)
        return hits

    def collide(self, walls, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, walls, False)
            if hits:
                if self.speed_x > 0:
                    self.rect.right = hits[0].rect.left
                if self.speed_x < 0:
                    self.rect.left = hits[0].rect.right
                self.speed_x = 0

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, walls, False)
            if hits:
                if self.speed_y > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.speed_y < 0:
                    self.rect.top = hits[0].rect.bottom
                self.speed_y = 0
