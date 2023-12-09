import pygame
import random
import os
from settings import *
from endless_vertical_platformer import *
from utils import *

# Inicializando o pygame
pygame.init()

# Criando a instância do jogador
jumpy = Jumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# Criando a plataforma inicial
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
platform_group.add(platform)

run = True
while run:
    
    clock.tick(FPS)
    
    if game_over == False:
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
            platform_type = random.randint(1, 2)
            if platform_type == 1 and score > 750:
                platform_movement = True
            else:
                platform_movement = False
            platform = Platform(platform_x, platform_y, platform_width, platform_movement)
            platform_group.add(platform)
        
        # Atualizando as plataformas
        platform_group.update(scroll)
        
        # Atualizando a pontuação
        if scroll > 0:
            score += scroll
            
        # Desenhando uma linha da pontuação maior
        pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3) 
        draw_text("HIGH SCORE", font_small, WHITE, SCREEN_WIDTH - 130, score - high_score + SCROLL_THRESH)
            
        # Desenhando sprites do player
        platform_group.draw(screen)
        jumpy.draw()
        
        # Desenhando o painel
        pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
        pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
        draw_text("SCORE: " + str(score), font_small, WHITE, 0, 0)
        
        # Verificando o fim do jogo
        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over = True
    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            # Construindo o fundo da imagem de game over
            for rect_y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, rect_y * 100, fade_counter, 100))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (rect_y + 1) * 100, SCREEN_WIDTH, 100))
        else:
            draw_text("GAME OVER", font_big, WHITE, 130, 200) 
            draw_text("SCORE: " + str(score), font_big, WHITE, 130, 250) 
            draw_text("PRESS SPACE TO PLAY AGAIN", font_big, WHITE, 40, 300)  
            # Atualizando a pontuação mais alta
            if score > high_score:
                high_score = score
                with open("score.txt", "w") as file:
                    file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # Redefinindo as variáveis
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                # Reposicionando o jogador
                jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                # Redefinindo as plataformas
                platform_group.empty()
                # Criando a plataforma inicial
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
                platform_group.add(platform)

    # Elaborando manipulador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Atualizando a pontuação mais alta
            if score > high_score:
                high_score = score
                with open("score.txt", "w") as file:
                    file.write(str(high_score))
            run = False
            

    # Atualizando a tela da janela
    pygame.display.update()   
pygame.quit()         