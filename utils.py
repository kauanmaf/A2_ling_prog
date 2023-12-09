import pygame


BACKGROUND = pygame.image.load("assets/menu-background.jpeg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)  