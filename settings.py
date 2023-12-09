import pygame
import os

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
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
background_scroll = 0
game_over = False
score = 0
fade_counter = 0

if os.path.exists("score.txt"):
    with open("score.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Definindo as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (184, 230, 253)

# Definindo as fontes
font_small = pygame.font.SysFont("Lucida Sans", 20)
font_big = pygame.font.SysFont("Lucida Sans", 24)

# Carregando imagens
jumper_image = pygame.image.load("endless_vertical_platformer_assets/jumper.png")
background_image = pygame.image.load("endless_vertical_platformer_assets/background.png")
platform_image = pygame.image.load("endless_vertical_platformer_assets/platform.png")

# Elaborando grupos de sprites
platform_group = pygame.sprite.Group()