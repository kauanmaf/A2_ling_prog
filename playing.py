import pygame, sys

from FlappyBird.FlappyBird_main import FlappyBird
from FlappyBird.settings_flappy import *

from FrogAdventure.frog_adventure_main import FrogJourneyGame

from utils import *


def playing_flappybird(screen):
    """
    Função que define as configurações necessárias e inicia o flappy bird

    :param surface screen: tela onde o jogo vai ser iniciado
    """
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
        
def playing_jumpman(scree):
    pass

def playing_frog():
    game = FrogJourneyGame()
    game.run()