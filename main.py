import pygame
from settings import *
from basic_jumper_classes import Jumper

# Inicializando o pygame
pygame.init()

# Criando a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Vertical")

jumpy = Jumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

while True:
    # Desenhando o plano de fundo
    screen.blit(bg_image, (0, 0))
    
    # Desenhando eventos do player
    jumpy.draw()

    # Elaborando manipulador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Atualizando a tela da janela
    pygame.display.update()        