import pygame

from Menu.menus import main_menu


pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))

main_menu(SCREEN)