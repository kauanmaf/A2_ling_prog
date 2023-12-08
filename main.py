import pygame
import random
from settings import *
from endless_vertical_platformer import *

# Inicializando o pygame
pygame.init()

# Criando a instância do jogador
jumpy = Jumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

run = True
while run:
    
    clock.tick(FPS)
    
    jumpy.move()
    
    # Desenhando o plano de fundo
    screen.blit(background_image, (0, 0))
    
    # Desenhando sprites do player
    platform_group.draw(screen)
    jumpy.draw()

    # Elaborando manipulador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Atualizando a tela da janela
    pygame.display.update()   
pygame.quit()         