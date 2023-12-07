import pygame

# Inicializando o pygame
pygame.init()

# Definindo as dimensões da janela do jogo
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 550

# Criando a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Definindo as cores
WHITE = (255, 255, 255)

# Carregando imagens
jumper_image = pygame.image.load("endless_vertical_platformer_assets/jumper.png")
bg_image = pygame.image.load("endless_vertical_platformer_assets/background.png")