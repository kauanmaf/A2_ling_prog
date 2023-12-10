import pygame
from settings import *

def draw_text(text, font, text_col, x, y ):
    """
    A função recebe parâmetros referentes a um texto e insere o texto na tela
    """
    text_image = font.render(text, True, text_col)
    screen.blit(text_image, (x, y))
    
def draw_panel():
    """
    A função desenha o painel de pontuação na tela do jogo
    """ 
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text("SCORE: " + str(score), font_small, WHITE, 0, 0)   

def draw_background(background_scroll):
    """
    A função recebe a variável de rolagem e constrói o desenho do plano de fundo
    """
    # Criando um plano de fundo infinito
    screen.blit(background_image, (0, 0 + background_scroll))
    screen.blit(background_image, (0, - 600 + background_scroll))