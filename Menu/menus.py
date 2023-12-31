import os
import sys
project_root = os.path.dirname(os.path.dirname(__file__)) 
sys.path.append(project_root)


import pygame, sys
from Menu.button import Button

from Menu.utils import *

from Menu.playing import playing_flappybird, playing_doodleman, playing_frog

pygame.init()

# tocando música de fundo do menu inicial em looping
pygame.mixer.music.load("Menu/menu_assets/pixel-perfect.mp3")
pygame.mixer.music.play(-1)

def main_menu(screen):
    """Função que cria o menu principal

    :param pygame.surface screen: tela na qual o menu vai ser criado
    """
    while True:
        # colocando background
        screen.blit(BACKGROUND, (0, 0))
        pygame.display.set_caption("Main menu")

        mouse_position = pygame.mouse.get_pos()

        text = get_font(100).render("MINI GAMES", True, "#d4a6a4")
        rect = text.get_rect(center=(640, 100))

        # criando botões
        play_buttton = Button(image=pygame.image.load("Menu/menu_assets/play-rect.png"), pos=(640, 275), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("Menu/menu_assets/quit-rect.png"), pos=(640, 475), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(text, rect)

        for button in [play_buttton, quit_button]:
            button.changeColor(mouse_position)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_buttton.checkForInput(mouse_position):
                    play(screen)
                if quit_button.checkForInput(mouse_position):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def play(screen):
    """Função que cria o menu no qual o jogador pode escolher entre os três jogos

    :param pygame.Surface screen: tela na qual criamos o menu
    """
    changed_screen = False
    while True:
        screen.blit(BACKGROUND, (0, 0))
        # screen.fill((0, 0, 0))
        pygame.display.set_caption("Games menu")

        mouse_position = pygame.mouse.get_pos()

        text = get_font(45).render("Choose your game", True, "#fafafa")
        rect = text.get_rect(center=(640, 60))
        screen.blit(text, rect)

        bird_img = pygame.image.load('Menu/menu_assets/bird.png').convert_alpha()
        jump_img = pygame.image.load('Menu/menu_assets/jumper-correct.png').convert_alpha()
        frog_img = pygame.image.load('Menu/menu_assets/froginho.png').convert_alpha()

        first_button = Button(image=bird_img, pos=(290, 360),
                              text_input="", font=get_font(45), base_color="#fafafa", hovering_color="#fafafa")
        second_button = Button(image=jump_img, pos=(600, 360),
                              text_input="", font=get_font(45), base_color="#fafafa", hovering_color="#fafafa")
        third_button = Button(image=frog_img, pos=(935, 360),
                              text_input="", font=get_font(45), base_color="#fafafa", hovering_color="#fafafa")

        back_button = Button(image=None, pos=(640, 650), 
                            text_input="BACK", font=get_font(75), base_color="#738fbf", hovering_color="Yellow")

        back_button.changeColor(mouse_position)
        
        first_button.update(screen)
        second_button.update(screen)
        third_button.update(screen)
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_position):
                    main_menu(screen)
                if first_button.checkForInput(mouse_position):
                    pygame.mixer.music.stop()
                    playing_flappybird(screen)
                if second_button.checkForInput(mouse_position):
                    changed_screen = True
                    pygame.mixer.music.stop()
                    # Tamanho da tela do jogo do doodle
                    pygame.display.set_mode((400, 600), pygame.RESIZABLE) 
                    playing_doodleman(screen)
                if third_button.checkForInput(mouse_position):
                    pygame.mixer.music.stop()
                    playing_frog()
            if changed_screen:
                    pygame.display.set_mode((1280, 720))
                    changed_screen = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                
                main_menu(screen)


        pygame.display.update()    

