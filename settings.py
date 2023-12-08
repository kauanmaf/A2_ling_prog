import pygame

# Inicializando o pygame
pygame.init()

# Definindo as dimensões da janela do jogo
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Criando a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Vertical")

# Definindo a taxa de quadros
clock = pygame.time.Clock()
FPS = 60

# Construindo as variáveis do jogo
GRAVITY = 1

# Definindo as cores
WHITE = (255, 255, 255)

# Carregando imagens
jumper_image = pygame.image.load("endless_vertical_platformer_assets/jumper.png")
bg_image = pygame.image.load("endless_vertical_platformer_assets/background.png")