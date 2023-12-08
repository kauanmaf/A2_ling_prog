import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))

BACKGROUND = pygame.image.load("assets/menu-background.jpeg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))
        pygame.display.set_caption("Games menu")

        mouse_position = pygame.mouse.get_pos()

        text = get_font(45).render("Choose your game", True, "#fafafa")
        rect = text.get_rect(center=(640, 60))
        SCREEN.blit(text, rect)

        bird_img = pygame.image.load('assets/bird.png').convert_alpha()
        snake_img = pygame.image.load('assets/snake.png').convert_alpha()
        # bird_img = pygame.image.load('assets/bird.png').convert_alpha()

        first_button = Button(image=bird_img, pos=(340, 360),
                              text_input="", font=get_font(45), base_color="#fafafa", hovering_color="#fafafa")
        second_button = Button(image=snake_img, pos=(700, 360),
                              text_input="", font=get_font(45), base_color="#fafafa", hovering_color="#fafafa")

        back_button = Button(image=None, pos=(640, 650), 
                            text_input="BACK", font=get_font(75), base_color="#d7fcb4", hovering_color="Yellow")

        back_button.changeColor(mouse_position)
        
        first_button.update(SCREEN)
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_position):
                    main_menu()

        pygame.display.update()      
    
def options():
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))
        pygame.display.set_caption("Options menu")

        mouse_position = pygame.mouse.get_pos()

        text = get_font(45).render("OPTIONS", True, "#fafafa")
        rect = text.get_rect(center=(640, 60))
        SCREEN.blit(text, rect)

        back_button = Button(image=None, pos=(640, 650),
                            text_input="BACK", font=get_font(75), base_color="#d7fcb4", hovering_color="Yellow")

        back_button.changeColor(mouse_position)
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_position):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))
        pygame.display.set_caption("Main menu")

        mouse_position = pygame.mouse.get_pos()

        text = get_font(100).render("MAIN MENU", True, "#b68f40")
        rect = text.get_rect(center=(640, 100))

        play_buttton = Button(image=pygame.image.load("assets/play-rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=pygame.image.load("assets/options-rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/quit-rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(text, rect)

        for button in [play_buttton, options_button, quit_button]:
            button.changeColor(mouse_position)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_buttton.checkForInput(mouse_position):
                    play()
                if options_button.checkForInput(mouse_position):
                    options()
                if quit_button.checkForInput(mouse_position):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()