from enum import Enum
import pygame

# Definindo as dimensões da tela do nosso jogo
screen_width = 1280
screen_height = 720

# Criando uma classe com cada minijogo e chamando pelo número
class Minigames_enum(Enum):
    "Classe com os jogos os quais iremos realizar."
    TETRIS = 0
    SPACE_INVADERS = 1
    PAC_MAN = 2
    FLAPPY_BIRD = 3


# Reponsável por armazenar os dados das posições
Tetris = {"posicao": (110, 400), "content": "this is Tetris", "unlock" : 1}
Space_invaders = {"posicao": (300, 220), "content": "this is space invader", "unlock" : 2}
Pac_man = {"posicao": (480, 610), "content": "this is pacman", "unlock" : 3}
Flappy_bird = {"posicao": (610, 350), "content": "this is flappy bird", "unlock" : 3}

minijogos_lista = {
    0: Tetris,
    1: Space_invaders,
    2: Pac_man,
    3: Flappy_bird,
}

# Images for flappy bird
#Images
bird_images = [pygame.image.load("flappy_bird_assets/bird_down.png"),
               pygame.image.load("flappy_bird_assets/bird_mid.png"), 
               pygame.image.load("flappy_bird_assets/bird_up.png")]

skyline_image = pygame.image.load("flappy_bird_assets/background.png")
ground_image = pygame.image.load("flappy_bird_assets/ground.png") 
top_pipe_image = pygame.image.load("flappy_bird_assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("flappy_bird_assets/pipe_bottom.png")
game_over_image = pygame.image.load("flappy_bird_assets/game_over.png")
start_image = pygame.image.load("flappy_bird_assets/start.png")