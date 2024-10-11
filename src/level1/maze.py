import pygame
import os
import random
from src.level1.win import WinScreen

from src.level1.camera import Camera

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, folder):
        super().__init__()
        self.images = [pygame.image.load(os.path.join(os.path.join("src/level1/portals", folder), f"sprite_{i}.png")).convert_alpha() for i in range(0, 9)]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_index = 0
        self.animation_timer = 0

    def update(self):
        self.animation_timer += 1
        if self.animation_timer >= 15:  # 3 frames/sec (assuming 60 FPS, 60/3=20)
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]

color_names = {
    '1': 'red',
    '2': 'green',
    '3': 'blue',
    '4': 'yellow',
    '5': 'purple',
}

class Maze:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.grid_size = 50
        self.walls = pygame.sprite.Group()
        self.codes = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.end = pygame.sprite.Group()
        self.portal_map = {}
        self.cooldown_time = 3000  # 3 seconds cooldown
        self.last_teleport_time = pygame.time.get_ticks()
        self.wall_image = pygame.image.load("src/level1/wall.png").convert_alpha()
        self.is_open = False
        self.show_popup = False
        self.code_reveal_popup = False
        self.correct_code = str(random.randint(1000, 9999))
        self.input_code = ""
        self.popup_rect = pygame.Rect((width - 300) // 2, (height - 200) // 2, 300, 200)
        self.close_button_rect = pygame.Rect(self.popup_rect.right - 50, self.popup_rect.top + 10, 40, 40)
        self.last_popup_close_time = pygame.time.get_ticks()
        self.partial_codes = []  
        self.sprite=None
        self.win_screen = WinScreen(screen, width, height)
        self.is_won = False
        self.win_screen_displayed = False
        self.start_time = None  
        self.load_level1('src/level.txt')


    def load_level1(self, level_file):
    
        with open(level_file, 'r') as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == '#':
                    wall = pygame.Surface((self.grid_size, self.grid_size))
                    wall.blit(self.wall_image, (0, 0))
                    wall_rect = wall.get_rect(topleft=(x * self.grid_size, y * self.grid_size))
                    wall_sprite = pygame.sprite.Sprite()
                    wall_sprite.image = wall
                    wall_sprite.rect = wall_rect
                    self.walls.add(wall_sprite)
                elif char in color_names:
                    portal = Portal(x * self.grid_size, y * self.grid_size, color_names[char])
                    self.portals.add(portal)
                    if char not in self.portal_map:
                        self.portal_map[char] = []
                    self.portal_map[char].append(portal)
                elif char == 'E':
                    end = pygame.Surface((self.grid_size, self.grid_size))
                    end.blit(self.wall_image, (0, 0))
                    end_rect = end.get_rect(topleft=(x * self.grid_size, y * self.grid_size))
                    end_sprite = pygame.sprite.Sprite()
                    end_sprite.image = end
                    end_sprite.rect = end_rect
                    self.end.add(end_sprite)
                elif char == 'N':

                    code = pygame.Surface((self.grid_size, self.grid_size))
                    code.blit(self.wall_image, (0, 0))
                    code_rect = code.get_rect(topleft=(x * self.grid_size, y * self.grid_size))
                    code_sprite = pygame.sprite.Sprite()
                    code_sprite.image = code
                    code_sprite.rect = code_rect
                    self.codes.add(code_sprite)
                    self.partial_codes.append(self.correct_code[:2])
                    self.partial_codes.append(self.correct_code[2:])
        self.win_screen.start_timer()

    def get_portals(self):
        return self.portals
    def get_codes(self):
        return self.codes
    def get_end(self):
        return self.end

    def on_portal_enter(self, portal, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_teleport_time > self.cooldown_time:
            self.last_teleport_time = current_time
            self.teleport_player(player, portal)
        else:
            portal.update()

    def check_win(self, player):
        end_sprite = self.end.sprites()[0]
        if player.rect.colliderect(end_sprite.rect):
            if not self.is_open and not self.show_popup and not self.code_reveal_popup:
                self.show_popup = True
                self.input_code = ""
            elif self.is_open==True:

               self.is_won = True
               self.win_screen.stop_timer()    
        code_sprite = self.codes.sprites()
        for sprite in code_sprite:
         if player.rect.colliderect(sprite.rect):
            if not self.is_open and not self.show_popup and not self.code_reveal_popup:
                self.sprite=sprite
                self.code_reveal_popup = True
              
              
    def handle_popup_events(self, event):
        if self.show_popup:
            self.handle_enter_code_popup_events(event)
        if self.code_reveal_popup:
            self.handle_code_reveal_popup_events(event)

    def handle_enter_code_popup_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.verify_code()
            elif event.key == pygame.K_BACKSPACE:
                self.input_code = self.input_code[:-1]
            elif len(self.input_code) < 4 and event.unicode.isdigit():
                self.input_code += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN :

            if self.close_button_rect.collidepoint(event.pos[0],event.pos[1]-150):
                self.show_popup = False
                self.last_popup_close_time = pygame.time.get_ticks()

    def handle_code_reveal_popup_events(self, event):
      
        if event.type == pygame.MOUSEBUTTONDOWN :

            if self.close_button_rect.collidepoint(event.pos[0],event.pos[1]-150):
                self.code_reveal_popup = False
                self.last_popup_close_time = pygame.time.get_ticks()

    def verify_code(self):
        if self.input_code == self.correct_code:
            self.is_open = True
        self.show_popup = False
        self.last_popup_close_time = pygame.time.get_ticks()

    def draw_popup(self):
        if self.show_popup:
            self.draw_enter_code_popup()
        elif self.code_reveal_popup:
            self.draw_code_reveal_popup()

    def draw_enter_code_popup(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.popup_rect, border_radius=5)
        inner_rect = self.popup_rect.inflate(-4, -4)
        pygame.draw.rect(self.screen, (207, 201, 200), inner_rect, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), self.close_button_rect, border_radius=5)
        inner_close_rect = self.close_button_rect.inflate(-4, -4)
        pygame.draw.rect(self.screen, (255, 0, 0), inner_close_rect, border_radius=5)
        font = pygame.font.Font(None, 36)
        close_text = font.render("X", True, (255, 255, 255))
        self.screen.blit(close_text, (inner_close_rect.x + (inner_close_rect.width - close_text.get_width()) // 2, inner_close_rect.y + (inner_close_rect.height - close_text.get_height()) // 2))
        text = font.render("Enter Code:", True, (0, 0, 0))
        self.screen.blit(text, (inner_rect.x + 20, inner_rect.y + 20))
        input_field_rect = pygame.Rect(inner_rect.x + 20, inner_rect.y + 60, 260, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), input_field_rect, border_radius=5)
        inner_input_field_rect = input_field_rect.inflate(-4, -4)
        pygame.draw.rect(self.screen, (50, 50, 50), inner_input_field_rect, border_radius=5)
        code_text = font.render(self.input_code, True, (255, 255, 255))
        self.screen.blit(code_text, (inner_input_field_rect.x + 10, inner_input_field_rect.y + 5))

    def draw_code_reveal_popup(self):
        
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_popup_close_time
        if elapsed_time < 500:  
            scale_factor = 1 + (0.2 * (elapsed_time / 500))  
            scaled_popup_rect = pygame.Rect(self.popup_rect.left, self.popup_rect.top, int(self.popup_rect.width * scale_factor), int(self.popup_rect.height * scale_factor))
        else:
            scaled_popup_rect = self.popup_rect

        self.screen.blit(pygame.image.load("src/level1/wall.png").convert_alpha(), self.popup_rect.topleft)
        pygame.draw.rect(self.screen, (0, 0, 0), scaled_popup_rect, border_radius=5)
        inner_rect = scaled_popup_rect.inflate(-4, -4)
        pygame.draw.rect(self.screen, (207, 201, 200), inner_rect, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), self.close_button_rect, border_radius=5)
        inner_close_rect = self.close_button_rect.inflate(-4, -4)
        pygame.draw.rect(self.screen, (255, 0, 0), inner_close_rect, border_radius=5)
        font = pygame.font.Font(None, 36)
        close_text = font.render("X", True, (255, 255, 255))
        self.screen.blit(close_text, (inner_close_rect.x + (inner_close_rect.width - close_text.get_width()) // 2, inner_close_rect.y + (inner_close_rect.height - close_text.get_height()) // 2))
        sprite_list=list(self.codes)
        code = self.partial_codes[sprite_list.index(self.sprite)]
        code_text = font.render(f"Code: {code}", True, (0, 0, 0))
        self.screen.blit(code_text, (inner_rect.x + 20, inner_rect.y + 20))

    def teleport_player(self, player, portal):
        for key, portal_pair in self.portal_map.items():
            if len(portal_pair) == 2:
                if portal == portal_pair[0]:
                    player.rect.topleft = portal_pair[1].rect.topleft
                elif portal == portal_pair[1]:
                    player.rect.topleft = portal_pair[0].rect.topleft

    def get_walls(self):
        return self.walls

    def update(self, player):
        if not self.show_popup and not self.code_reveal_popup and self.can_show_popup():
            self.check_win(player)
        self.draw_popup()

    def can_show_popup(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_popup_close_time > self.cooldown_time
