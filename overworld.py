import pygame
from game_data import niveis

class Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=pos)

class Overworld:
    def __init__(self, start_level, max_level, surface):
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

        # sprites
        self.create_nodes()

    def create_nodes(self):
        self.nodes = pygame.sprite.Group() 

        for node_data in niveis.values():
            node_sprite = Node(node_data["posicao"])
            self.nodes.add(node_sprite)

    def run(self):
        self.nodes.draw(self.display_surface)
