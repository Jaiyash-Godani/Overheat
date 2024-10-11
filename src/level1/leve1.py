import pygame
from src.level1.player import Player
from src.level1.maze import Maze
from src.level1.camera import Camera
from src.level1.win import WinScreen


def setup_level1(screen,screen_width, screen_height):
    player = Player(100, 250)
    maze = Maze(screen,screen_width, screen_height)
    camera = Camera(screen_width, screen_height)
    win = WinScreen(screen,screen_width, screen_height)
    win.start_timer()
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(maze.get_walls())
    # all_sprites.add(*maze.get_portal())
    
    custom_group = pygame.sprite.Group()
    custom_group.add(maze.get_portals())

    code_group = pygame.sprite.Group()
    code_group.add(maze.get_codes())

    end_group = pygame.sprite.Group()
    end_group.add(maze.get_end())

    return player, maze, camera,win, all_sprites, custom_group,end_group,code_group

def handle_player_movement(event, player,maze):
   
    if maze.show_popup or maze.code_reveal_popup:
            
            maze.handle_popup_events(event)

       
    if event.type == pygame.KEYDOWN:
      if not maze.show_popup:
        if event.key in [pygame.K_LEFT, pygame.K_a]:
            player.move_left()
        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
            player.move_right()
        elif event.key in [pygame.K_UP, pygame.K_w]:
            player.move_up()
        elif event.key in [pygame.K_DOWN, pygame.K_s]:
            player.move_down()
    elif event.type == pygame.KEYUP:
        if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
            player.stop()

    

def update_level1(player, maze, camera,win, all_sprites, custom_group,end_group, code_group,screen):
    # Update all sprites
    
    all_sprites.update(maze.get_walls())
    custom_group.update()
    code_group.update()
    player.update(maze.get_walls())
    end_group.update()
    if not maze.is_open and maze.can_show_popup():
      maze.check_win(player)

    # Update camera
    
    camera.update(player)
    # Clear the screen
    screen.fill((0, 0, 0))

    if not maze.is_won:
        for entity in all_sprites:
            screen.blit(entity.image, camera.apply(entity))
        for entity in custom_group:
            screen.blit(entity.image, camera.apply(entity))
        for entity in end_group:
            screen.blit(entity.image, camera.apply(entity))
        for entity in code_group:
            screen.blit(entity.image, camera.apply(entity))
            maze.update(player)
            screen.blit(player.image, camera.apply(player))
    else:
            win.stop_timer()
            win.draw_win_screen()
       
    hit_portals = player.is_on_portal(custom_group)
    if hit_portals:
        for portal in hit_portals:
            maze.on_portal_enter(portal,player)

