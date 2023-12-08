import pygame
from settings import *

def draw_background(background_scroll):
    """
    A função recebe a variável de rolagem e realizar o desenho do plano de fundo
    """
    # Criando um plano de fundo infinito
    screen.blit(background_image, (0, 0 + background_scroll))
    screen.blit(background_image, (0, - 600 + background_scroll))