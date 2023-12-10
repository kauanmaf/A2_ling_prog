import os
import sys
import pygame

project_root = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(project_root)


BACKGROUND = pygame.image.load("Menu/menu_assets/menu-background.jpeg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Menu/menu_assets/font.ttf", size)  