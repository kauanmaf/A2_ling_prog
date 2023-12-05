import pygame
from settings import *
from abstract import Minigame_abs
import sys

pygame.init()

class Flappy_bird(Minigame_abs):
    def __init__(self, current_level, surface, create_level_map):
        super().__init__()
        # level setup
        self.display_surface = surface
        self.current_level = current_level
        level_data = minijogos_lista[current_level]
        level_content = level_data["content"]
        self.new_max_level = level_data["unlock"]
        self.create_level_map = create_level_map
        
        # level display
        self.font = pygame.font.Font(None, 40)
        self.text_surf = self.font.render(level_content, True, "White")
        self.text_rect = self.text_surf.get_rect(center=(screen_width/2, screen_height/2))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_level_map(self.current_level, self.new_max_level)

        if keys[pygame.K_ESCAPE]:
            self.create_level_map(self.current_level, 0)

    def run(self):
        self.input()
        self.display_surface.blit(self.text_surf, self.text_rect)

class Minigame():
    def __init__(self, current_level, surface, create_level_map):
        # level setup
        self.display_surface = surface
        self.current_level = current_level
        level_data = minijogos_lista[current_level]
        level_content = level_data["content"]
        self.new_max_level = level_data["unlock"]
        self.create_level_map = create_level_map
        
        # level display
        self.font = pygame.font.Font(None, 40)
        self.text_surf = self.font.render(level_content, True, "White")
        self.text_rect = self.text_surf.get_rect(center=(screen_width/2, screen_height/2))

    def run_minigame(self):
    
        if int(self.current_level) == 0:
            Flappy_bird_instance = Flappy_bird(self.current_level, self.display_surface, self.create_level_map)

            # Run TETRIS minigame
            Flappy_bird_instance.run()
        elif self.current_level == 1:
            # Run SPACE_INVADERS minigame
            print("Running SPACE_INVADERS minigame")
        elif self.current_level == 2:
            # Run PAC_MAN minigame
            print("Running PAC_MAN minigame")
        elif self.current_level == 3:
            # Run FLAPPY_BIRD minigame
            print("Running FLAPPY_BIRD minigame")
