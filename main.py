import pygame
import random
from settings import *
from endless_vertical_platformer import *
from utils import draw_background

# Inicializando o pygame
pygame.init()

# Criando a instância do jogador
jumpy = Jumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

run = True
while run:
    
    clock.tick(FPS)
    
    scroll = jumpy.move()
   
    # Desenhando o plano de fundo
    background_scroll += scroll
    if background_scroll >= 600:
        # Redefinindo a rolagem da imagem de fundo
        background_scroll = 0
    draw_background(background_scroll)
    
    # Desenhando limite de rolagem temporário
    pygame.draw.line(screen, WHITE, (0, SCROLL_THRESH), (SCREEN_WIDTH, SCROLL_THRESH))
    
    # Atualizando as plataformas
    platform_group.update(scroll)
    
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