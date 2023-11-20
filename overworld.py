from typing import Any
import pygame
from game_data import niveis

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == "available":
            self.image.fill("red")
        else: 
            self.image.fill("grey")

        self.rect = self.image.get_rect(center=pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2),icon_speed,icon_speed)

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20,20))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self, start_level, max_level, surface):
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

        # movement logic
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.moving = False

        # sprites
        self.create_nodes()
        self.setup_icon()

    def create_nodes(self):
        self.nodes = pygame.sprite.Group() 

        for index, node_data in enumerate(niveis.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data["posicao"], "available", self.speed)
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_data["posicao"], "locked", self.speed)
            self.nodes.add(node_sprite)
    def draw_paths(self):
        centers = []
        for index, node_data in enumerate(niveis.values()):
            if index <= self.max_level:
                centers.append(node_data["posicao"])
            
        pygame.draw.lines(self.display_surface, "red", False, centers, 6)
    
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        if not self.moving:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data("next")
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data("previous")
                self.current_level -= 1
                self.moving = True

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == "next":
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()
    
    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        
