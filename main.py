import pygame
from settings import *
from basic_jumper_classes import Jumper

# Inicializando o pygame
pygame.init()

jumpy = Jumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

run = True
while run:
    
    clock.tick(FPS)
    
    jumpy.move()
    
    # Desenhando o plano de fundo
    screen.blit(bg_image, (0, 0))
    
    # Desenhando eventos do player
    jumpy.draw()

    # Elaborando manipulador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Atualizando a tela da janela
    pygame.display.update()   
pygame.quit()         