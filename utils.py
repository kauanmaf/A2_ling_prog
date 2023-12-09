import pygame


BACKGROUND = pygame.image.load("menu_assets/menu-background.jpeg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("menu_assets/font.ttf", size)  