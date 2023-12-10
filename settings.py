import pygame
import os

# Inicializando o pygame
pygame.init()

# Definindo as dimensões da janela do jogo
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Criando a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump")

# Definindo a taxa de quadros
clock = pygame.time.Clock()
FPS = 60

# Carregando músicas e sons
background_music = pygame.mixer.music.load("endless_vertical_platformer_assets/music.mp3")
# background_music.set_volume(0.6)
# background_music.play(- 1, 0.0)
death_sound = pygame.mixer.Sound("endless_vertical_platformer_assets/death.mp3")
death_sound.set_volume(0.5)

# Construindo as variáveis do jogo
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
# scroll = 0
# background_scroll = 0
# game_over = False
# score = 0
# fade_counter = 0

# if os.path.exists("score.txt"):
#     with open("score.txt", "r") as file:
#         high_score = int(file.read())
# else:
#     high_score = 0

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

# Carregando a imagem do inimigo
enemy_sheet_image = pygame.image.load("endless_vertical_platformer_assets/enemy.png")

# # Elaborando grupos de sprites
# platform_group = pygame.sprite.Group()
# enemy_group = pygame.sprite.Group()