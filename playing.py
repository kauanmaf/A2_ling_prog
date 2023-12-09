import pygame, sys

from FlappyBird import FlappyBird
from settings import *

from utils import *


BACKGROUND = pygame.image.load("assets/menu-background.jpeg")


def playing_flappybird(screen):
    pygame.display.set_caption("Flappy Bird")
    
    clock = pygame.time.Clock()
    game = FlappyBird(screen)

    while True:
        # Configurando a taxa de atualização do jogo
        clock.tick(100)

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
        

def playing_jumpman(screen):
    while True:
        screen.fill((252, 25, 192))

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()