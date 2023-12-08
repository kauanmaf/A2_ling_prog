import pygame
import random
from settings import *
from endless_vertical_platformer import *
from utils import draw_background

# Inicializando o pygame
pygame.init()

# Criando a instância do jogador
jumpy = Jumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# Criando a plataforma inicial
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)

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
    
    # Gerando plataformas
    if len(platform_group) < MAX_PLATFORMS:
        platform_width = random.randint(40, 60)
        platform_x = random.randint(0, SCREEN_WIDTH - platform_width)
        platform_y = platform.rect.y - random.randint(80, 120)
        platform = Platform(platform_x, platform_y, platform_width)
        platform_group.add(platform)
    
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