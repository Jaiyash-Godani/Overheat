import pygame
import time

class WinScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.timer_started = False
        self.start_time = None
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
    
    def start_timer(self):
        self.timer_started = True
        self.start_time = pygame.time.get_ticks()

    def stop_timer(self):
        self.timer_started = False

    def get_formatted_time(self):
        if not self.timer_started or self.start_time is None:
           
            elapsed_time = pygame.time.get_ticks() - self.start_time
            seconds = elapsed_time // 1000
            milliseconds = (elapsed_time % 1000) // 10
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes:02}:{seconds:02}.{milliseconds:02}"

    def draw_win_screen(self):
        self.screen.fill((0, 0, 0))
        win_text = self.font.render("You Win!", True, (255, 255, 255))
        self.screen.blit(win_text, (self.width // 2 - win_text.get_width() // 2, self.height // 2 - win_text.get_height() // 2 - 50))
        
        time_text = self.small_font.render(f"Time: {self.get_formatted_time()}", True, (255, 255, 255))
        self.screen.blit(time_text, (self.width // 2 - time_text.get_width() // 2, self.height // 2 + 50))
