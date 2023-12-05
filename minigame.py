import pygame
from settings import *
from abstract import Minigame_abs
from flappy_bird import FlappyBird


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

         # Create an instance of the game based on the current level
        if int(self.current_level) == 0:
            self.current_game = FlappyBird(self.display_surface)
        elif self.current_level == 1:
            # Create an instance of SPACE_INVADERS game
            print("Creating SPACE_INVADERS game")
            self.current_game = None  # Replace with the actual instance
        elif self.current_level == 2:
            # Create an instance of PAC_MAN game
            print("Creating PAC_MAN game")
            self.current_game = None  # Replace with the actual instance
        elif self.current_level == 3:
            # Create an instance of FLAPPY_BIRD game
            print("Creating FLAPPY_BIRD game")
            self.current_game = None  # Replace with the actual instance

    def run_minigame(self):
        self.current_game.run()
        
