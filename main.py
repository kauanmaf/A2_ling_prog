import pygame

# Inicializando o pygame
pygame.init()

# Definindo as dimensões da janela do jogo
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Carregando imagens

bg_image = pygame.image.load("endless_vertical_platformer_assets/background.png").convert_alpha()

# Criando a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Vertical")

while True:
    # Desenhando o plano de fundo
    screen.blit(background.png, (0, 0))

    # Elaborando manipulador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Atualizando a tela da janela
    pygame.display.update()        