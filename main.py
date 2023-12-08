import pygame
from settings import *
from FlappyBird import FlappyBird
import sys


# Configurando o jogo                                     
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = FlappyBird(screen)

# Adicionando nome
pygame.display.set_caption("Mini Arcade")

# making the loop while to start
while True:
    # Configurando a taxa de atualização do jogo
    clock.tick(60)

    # Configurando o fundo da tela
    screen.fill((0, 0, 0))

    # Criando uma instância do jogo
    game.run()

    # Loop for para casa a pessoa queira sair do jogo
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Fazendo um update pra manter no caso de atualizações
    pygame.display.update()