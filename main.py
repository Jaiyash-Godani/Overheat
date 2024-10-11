import pygame
import sys
import asyncio
from src.level1.leve1 import setup_level1, handle_player_movement, update_level1

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1000, 650
game = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Castle Rushout")
screen = pygame.Surface((screen_width, screen_height-150))

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Setup the first level
player, maze, camera,win, all_sprites, custom_group,end_group,code_group = setup_level1(screen,screen_width, screen_height)


async def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle_player_movement(event, player,maze)

    
        update_level1(player, maze, camera,win, all_sprites, custom_group, end_group,code_group,screen)



  
        game.blit(screen, (0, 150))
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
        await asyncio.sleep(0)
asyncio.run(main())        
pygame.quit()
sys.exit()
